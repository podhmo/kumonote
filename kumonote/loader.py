import yaml
from . import dictlib


class YAMLLoader:
    def load(self, path):
        with open(path) as rf:
            return yaml.load(rf)

    def merge(self, data, path):
        return dictlib.deep_merge(data, self.load(path))
