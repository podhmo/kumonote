import time
import asyncio
import logging
logger = logging.getLogger(__name__)


class Fetcher:
    def __init__(self, app):
        self.app = app
        self.get_response = app.resolver.resolve_object(app.config["fetcher"]["get_response"])

    async def fetch(self, request):
        return await self.get_response(request)


class LimittedFetcher:
    def __init__(self, app):
        self.app = app
        same_domain_limit = app.config["fetcher"]["same_domain_limit"]
        get_key = app.resolver.resolve_object(app.config["fetcher"]["get_key"])
        self.dispatcher = LimitterDispatcher(get_key, same_domain_limit)
        self.get_response = app.resolver.resolve_object(app.config["fetcher"]["get_response"])

    async def fetch(self, request):
        return await self.dispatcher.dispatch(self.get_response, request)


class Limitter:
    def __init__(self, domain, limit=2):
        self.domain = domain
        self.limit = limit
        self.delta = 1
        self.waittime = 1
        self.semaphore = asyncio.Semaphore(limit)

        self.count = 0
        self.last_called_at = None

    async def __call__(self, fn, *args, **kwargs):
        async with self.semaphore:
            logger.info("L request: %s", self.domain)
            t = time.time()
            self.count += 1
            if self.count >= self.limit and self.last_called_at and (t - self.last_called_at) < self.delta:
                await self.wait()
            self.last_called_at = t
            result = await fn(*args, **kwargs)
            self.count -= 1
            return result

    async def wait(self):
        logger.info("L *wait**: %s, waittime=%s, (%s/%s)", self.domain, self.waittime, self.count, self.limit)
        await asyncio.sleep(self.waittime)


class LimitterDispatcher:
    limitter_factory = Limitter

    def __init__(self, get_key, limit_count=2):
        self.cache = {}  # domain -> limitter
        self.get_key = get_key
        self.limit_count = limit_count

    def dispatch(self, fn, value, *args, **kwargs):
        key = self.get_key(value)
        limitter = self.cache.get(key)
        if limitter is None:
            self.cache[key] = limitter = self.create_limitter(key)
        return limitter(fn, value, *args, **kwargs)

    def create_limitter(self, key):
        return self.limitter_factory(key, limit=self.limit_count)
