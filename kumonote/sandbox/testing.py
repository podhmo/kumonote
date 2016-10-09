import asyncio
import logging
logger = logging.getLogger(__name__)


class MockRequest:
    # actually url -> response
    # mock request -> mock response (same object)
    def __init__(self, url, links=None):
        self.url = url
        self.links = links or []

    async def get_links(self):
        logger.info("R get link start: %s, cost=%s", self.url, 0.1)
        await asyncio.sleep(0.1)
        logger.info("R get link end  : %s", self.url)
        return self.links

    async def fetch(self):
        d = 0.2  # * random.random()
        logger.info("R fetch start   : %s, cost=%s", self.url, d)
        await asyncio.sleep(d)
        logger.info("R fetch end     : %s", self.url)
        response = self  # this is dummy, so...
        return response

    def __repr__(self):
        return r'MockRequest<url={!r}, links={}>'.format(self.url, len(self.links))


async def mock_fetch(request):
    return await request.fetch()


class MockRequestTreeBuilder:
    def build(self, d, path=None):
        """
        input format sample
        {"a": [{"a/b": []}, {"a/c": []}]}
        """
        path = path or []
        if isinstance(d, str):
            return [MockRequest(d)]
        elif hasattr(d, "items"):
            requests = []
            for url, chilren in d.items():
                request = MockRequest(url)
                path.append(url)
                try:
                    for sub in chilren:
                        request.links.extend(self.build(sub, path=path))
                except TypeError as e:
                    raise ValueError("expected list but {}. (in {})\noriginal: {}".format(chilren, path, e))
                path.pop()
                requests.append(request)
            return requests
        elif isinstance(d, (list, tuple)):
            path.append("[]")
            result = [self.build(x) for x in d]
            path.pop()
            return result
        else:
            raise TypeError("invalid value: {}".format(d))
