import time
from contextlib import contextmanager

@contextmanager
def timer_ms():
    start = time.perf_counter()
    yield lambda: (time.perf_counter() - start) * 1000

def get_risk_level(score: float) -> str:
    if score >= 0.70:
        return "HIGH"
    elif score >= 0.35:
        return "MEDIUM"
    else:
        return "LOW"