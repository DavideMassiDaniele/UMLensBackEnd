import os
import json


class PatternRequest:

    def __init__(self, filepath, filters, config_filepath):
        self.filepath = filepath
        self.filters = filters
        self.config_filepath = config_filepath

    @staticmethod
    def get_valid_filters():
        return ['abstractfactory', 'adapter', 'bridge', 'composite', 'decorator', 'facade', 'factorymethod', 'prototype', 'proxy', 'singleton']

    def get_filters(self):
        return f"-p {' '.join(self.filters)}" if len(self.filters) > 0 else ''

    def get_output_file(self, mode):
        filename, _ = os.path.splitext(self.filepath)
        return f'{filename}_{mode}.json'

    def generate_output(self, mode):
        os.system(f'python3 umlens/umlens.py {mode} -i {self.filepath} -o {self.get_output_file(mode)} {self.get_filters() if mode == "patterns" else ""} {("-c " + self.config_filepath) if mode == "metrics" else ""}')

    def generate_output_and_parse(self, mode):
        self.generate_output(mode)
        with open(self.get_output_file(mode)) as jsonFile:
            data = json.load(jsonFile)
            jsonFile.close()
        self.clear_output(mode)
        return data

    def clear_output(self, mode):
        os.remove(self.get_output_file(mode))

    def get_patterns(self):
        return self.generate_output_and_parse('patterns')

    def get_cycles(self):
        return self.generate_output_and_parse('cycles')

    def get_metrics(self):
        return self.generate_output_and_parse('metrics')
