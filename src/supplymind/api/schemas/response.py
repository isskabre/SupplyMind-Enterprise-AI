"""Standard API response schemas."""

from typing import Generic, TypeVar

from pydantic import BaseModel


DataT = TypeVar("DataT")


class ApiResponse(BaseModel, Generic[DataT]):
    """
    Standard successful API response.

    Attributes:
        success: Indicates whether the operation succeeded.
        message: Human-readable description of the result.
        data: Structured response payload.
    """

    success: bool = True
    message: str
    data: DataT