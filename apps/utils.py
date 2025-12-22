import time
from contextlib import contextmanager

@contextmanager
def timer_ms():
    start = time.perf_counter()
    yield lambda: (time.perf_counter() - start) * 1000
