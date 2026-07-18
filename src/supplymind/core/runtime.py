"""
SupplyMind Enterprise AI

Application Runtime Information

Provides process-level runtime metadata such as application uptime.
"""

import time


_PROCESS_START_TIME_NS = time.monotonic_ns()


def get_uptime_seconds() -> float:
    return (
        time.monotonic_ns() - _PROCESS_START_TIME_NS
    ) / 1_000_000_000