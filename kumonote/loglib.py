import logging
import time
logger = logging.getLogger(__name__)


class Extension:
    def __init__(self):
        self.start_time = time.time()

    def elapsed_time(self):
        return time.time() - self.start_time


class LogRecordExtension(logging.LogRecord):
    extension = Extension()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elapsed_time = self.extension.elapsed_time()
