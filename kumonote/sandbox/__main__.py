import os.path
import argparse
import importlib
import logging
from kumonote.loader import YAMLLoader


logger = logging.getLogger(__name__)


class Resolver:
    def resolve_object(self, path):
        module, attr_name = path.rsplit(":", 1)
        m = self.resolve_module(module)
        return getattr(m, attr_name)

    def resolve_module(self, path):
        return importlib.import_module(path)

    def resolve_location(self, target):
        base, path = target.split("/", 1)
        cwd = self.resolve_module(base).__path__[0]
        return os.path.join(cwd, path)


class App:
    def __init__(self, config):
        self.resolver = Resolver()
        self.config = config
        assert config["basic"]["path_type"] == "module"

    def load_requests(self, data):
        # data: file, path_type, loader, builder
        assert "srcfile" in data
        assert "loader" in data
        assert "builder" in data

        path = self.resolver.resolve_location(data["srcfile"])
        loader = self.resolver.resolve_object(data["loader"])()
        builder = self.resolver.resolve_object(data["builder"])()
        return builder.build(loader.load(path))

    def load_logging(self, data):
        if data is None:
            return
        fmt = data.get("format")
        level = getattr(logging, data.get("level").upper(), None)
        logging.basicConfig(format=fmt, level=level)
        # if fmt:
        #     logging.root.handlers[0].setFormatter(logging.Formatter(fmt=fmt))
        # if level:
        #     logging.root.handlers[0].setLevel(level)
        #     logging.root.setLevel(level)

    def run(self):
        config = self.config

        self.load_logging(config.get("logging"))
        requests = self.load_requests(config["target_request"])
        main = self.resolver.resolve_object(config["driver"]["main"])
        return main(self, requests)


def generate_config():
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "sample-config.yaml")) as rf:
        print(rf.read())


def main():
    # config, init=False
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=True)
    parser.add_argument("--override", required=False, nargs="*", default=[])
    parser.add_argument("--init", default=False, action="store_true")
    args = parser.parse_args()
    if args.init:
        return generate_config()

    path = os.path.normpath(os.path.abspath(args.config))
    if not os.path.exists(path):
        return generate_config()
    loader = YAMLLoader()
    config = loader.load(path)
    for override_path in args.override:
        config = loader.merge(config, override_path)
    return App(config).run()

if __name__ == "__main__":
    main()
