import yaml
import asyncio
# actually url -> response
# mock request -> mock response (same object)


class MockRequest:
    def __init__(self, url, links=None):
        self.url = url
        self.links = links or []

    async def get_links(self):
        await asyncio.sleep(0.1)
        return self.links

    def __repr__(self):
        return r'MockRequest<url={!r}, links={}>'.format(self.url, len(self.links))


class MockRequestTreeBuilder:
    def build_from_object(self, d):
        """
        input format sample
        {"a": [{"a/b": []}, {"a/c": []}]}
        """
        if isinstance(d, str):
            return MockRequest(d)
        elif hasattr(d, "items"):
            requests = []
            for url, chilren in d.items():
                request = MockRequest(url)
                for sub in chilren:
                    request.links.append(self.build_from_object(sub))
                requests.append(request)
            return requests
        elif isinstance(d, (list, tuple)):
            return [self.build_from_object(x) for x in d]
        else:
            raise TypeError("invalid value: {}".format(d))

    def build_from_yaml_file(self, path):
        with open(path) as rf:
            data = yaml.load(rf)
        return self.build_from_object(data)


if __name__ == "__main__":
    path = "./data/sample-requests.yaml"
    requests = MockRequestTreeBuilder().build_from_yaml_file(path)
    print(requests)
