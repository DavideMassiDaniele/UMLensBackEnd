import uuid
import os
from pathlib import Path
import concurrent.futures

from flask import Flask
from flask import request
from flask_cors import CORS

from .extensions.class_diagram.diagram_viewer.app.diagram_viewer import get_diagram
from .extensions.sequence_diagrams.sequence_diagrams import SequenceDiagramParser

from .model.ApiInfo import ApiInfo
from .model.ApiResponse import ApiResponse
from .model.PatternRequest import PatternRequest

app = Flask(__name__)

CORS(app)

# Prepare `umlens` directory under /tmp
Path("/tmp/umlens").mkdir(parents=True, exist_ok=True)


@app.route("/api/info")
def index():
    info = ApiInfo("1.0")
    return info.get_info()


@app.route("/api/filters")
def filter_list():
    return ApiResponse.success(PatternRequest.get_valid_filters())


@app.route("/api/pattern", methods=['POST'])
def pattern():
    print("Sono dentro il server")
    # Get input file
    file = request.files.get('file')
    if not file:
        return ApiResponse.bad_request()

    # Get config file
    config_file = request.files.get('config')
    if not config_file:
        
        return ApiResponse.bad_request()

    # Get all filters
    filters = request.form.getlist('filter[]')

    # Check for valid filters
    if any([input_filter not in PatternRequest.get_valid_filters() for input_filter in filters]):
        return ApiResponse.bad_request()

    # Generate filepath for input file and config file
    _uuid = uuid.uuid4().hex
    filename, file_extension = os.path.splitext(file.filename)
    filepath = f"/tmp/umlens/{filename}_{_uuid}{file_extension}"

    config_filename, config_file_extension = os.path.splitext(config_file.filename)
    config_filepath = f"/tmp/umlens/{config_filename}_{_uuid}{config_file_extension}"

    # Save file to tmp dir
    file.save(filepath)
    file.close()

    # Save config file to tmp dir
    config_file.save(config_filepath)
    config_file.close()

    # Process data and build response
    pattern_request = PatternRequest(filepath, filters, config_filepath)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(pattern_request.get_patterns),
            executor.submit(pattern_request.get_cycles),
            executor.submit(pattern_request.get_metrics)
        ]
        patterns, cycles, metrics = [f.result() for f in futures]

    response = ApiResponse.success({
        'diagram': get_diagram(filepath).decode("utf-8"),
        'patterns': patterns,
        'cycles': cycles,
        'metrics': metrics
    })

    # Remove file from tmp dir
    os.remove(filepath)

    return response


@app.route("/api/sequence-diagram", methods=['POST'])
def sequence_diagram():

    # Get input file
    file = request.files.get('file')
    if not file:
        return ApiResponse.bad_request()

    # Generate filepath for input file and config file
    _uuid = uuid.uuid4().hex
    filename, file_extension = os.path.splitext(file.filename)
    filepath = f"/tmp/umlens/{filename}_{_uuid}{file_extension}"

    # Save file to tmp dir
    file.save(filepath)
    file.close()

    sdp = SequenceDiagramParser(filepath)

    return ApiResponse.success(sdp.get_metrics())
