"""
Tests for request logging middleware behavior.
"""

import logging

from supplymind.middleware.request_logging import _get_log_level


def test_success_status_uses_info_level() -> None:
    assert _get_log_level(200) == logging.INFO
    assert _get_log_level(301) == logging.INFO
    assert _get_log_level(399) == logging.INFO


def test_client_error_status_uses_warning_level() -> None:
    assert _get_log_level(400) == logging.WARNING
    assert _get_log_level(404) == logging.WARNING
    assert _get_log_level(499) == logging.WARNING


def test_server_error_status_uses_error_level() -> None:
    assert _get_log_level(500) == logging.ERROR
    assert _get_log_level(503) == logging.ERROR
    assert _get_log_level(599) == logging.ERROR