# -*- coding:utf-8 -*-
import time
import asyncio
import logging
logger = logging.getLogger(__name__)


async def do_loop_single_chain(requests, fetch):
    todo = []
    done = []
    st = time.time()
    todo.extend(requests)
    while todo:
        r = todo.pop()
        response = await fetch(r)
        logger.info("sleep 1")
        await asyncio.sleep(1)
        done.append(r)
        todo.extend(await response.get_links())
    logger.info("takes %s, total %s", time.time() - st, len(done))
