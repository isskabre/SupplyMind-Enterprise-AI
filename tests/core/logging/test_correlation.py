"""
Tests for correlation ID validation and generation.
"""

from uuid import UUID

from supplymind.core.logging.correlation import (
    is_valid_correlation_id,
    resolve_correlation_id,
)


def test_valid_correlation_id_is_accepted() -> None:
    correlation_id = "gateway-request_123.abc"

    assert is_valid_correlation_id(correlation_id) is True


def test_missing_correlation_id_is_rejected() -> None:
    assert is_valid_correlation_id(None) is False


def test_empty_correlation_id_is_rejected() -> None:
    assert is_valid_correlation_id("") is False


def test_correlation_id_with_spaces_is_rejected() -> None:
    assert is_valid_correlation_id("request id") is False


def test_correlation_id_with_line_break_is_rejected() -> None:
    assert is_valid_correlation_id("request-123\nforged-log") is False


def test_valid_correlation_id_is_preserved() -> None:
    correlation_id = "existing-request-123"

    assert resolve_correlation_id(correlation_id) == correlation_id


def test_invalid_correlation_id_is_replaced_with_uuid() -> None:
    generated_id = resolve_correlation_id("unsafe request id")

    assert UUID(generated_id)
