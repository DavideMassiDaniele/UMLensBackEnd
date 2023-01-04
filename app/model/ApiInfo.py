from flask import jsonify as json


class ApiInfo:

    def __init__(self, version):
        self.version = version

    def get_info(self):
        return json({
            'version': self.version,
            'status': 'healthy'
        })
