# -*- coding:utf-8 -*-
from contextlib import closing


def main(app, requests):
    resolve = app.resolver.resolve_object
    with closing(resolve(app.config["driver"]["loop"])()) as loop:
        loop_main = resolve(app.config["driver"]["loop_main"])
        fetch = resolve(app.config["driver"]["fetcher"])(app).fetch
        loop.run_until_complete(loop_main(requests, fetch))
