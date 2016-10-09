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
        done.append(r)
        todo.extend(await response.get_links())
    logger.info("takes %s, total %s", time.time() - st, len(done))


async def do_loop_concurrently(requests, fetch):
    todo = []
    st = time.time()
    todo.extend(requests)
    running = []
    done = []

    def callback(fut):
        running.pop()
        running.append(object)
        fut2 = asyncio.ensure_future(fut.result().get_links())
        fut2.add_done_callback(callback2)

    def callback2(fut):
        todo.extend(fut.result())
        running.pop()
        done.append(object())

    while todo or running:
        targets = todo[:]
        todo.clear()
        for req in targets:
            fut = asyncio.ensure_future(fetch(req))
            running.append(object())
            fut.add_done_callback(callback)
        await asyncio.sleep(0.2)
    logger.info("takes %s, total %s", time.time() - st, len(done))
