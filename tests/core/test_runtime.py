"""
Tests for application runtime information.
"""

import time

from supplymind.core.runtime import get_uptime_seconds


def test_uptime_is_non_negative() -> None:
    """Application uptime should never be negative."""

    assert get_uptime_seconds() >= 0


def test_uptime_increases_over_time() -> None:
    """Application uptime should increase as time passes."""

    first_uptime = get_uptime_seconds()

    time.sleep(0.05)

    second_uptime = get_uptime_seconds()

    assert second_uptime > first_uptime
