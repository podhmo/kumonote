import yaml


class YAMLLoader:
    def load(self, path):
        with open(path) as rf:
            return yaml.load(rf)
