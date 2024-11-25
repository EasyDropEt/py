from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class BaseResponse(Generic[T]):
    def __init__(
        self, is_success: bool, message: str, data: Optional[T], errors: list[str]
    ):
        self.is_success = is_success
        self.message = message
        self.data = data
        self.errors = errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_success": self.is_success,
            "message": self.message,
            "data": self.data,
            "errors": self.errors,
        }

    @classmethod
    def success(cls, message: str, data: Optional[T] = None) -> "BaseResponse[T]":
        return cls(is_success=True, message=message, data=data, errors=[])

    @classmethod
    def error(cls, message: str, errors: list[str]) -> "BaseResponse[T]":
        return cls(is_success=False, message=message, data=None, errors=errors)


T = TypeVar("T")


class ApiResponse(BaseModel):
    success: bool = Field(...)
    message: str = Field(...)


class GenericResponse(ApiResponse, Generic[T]):
    data: Optional[T] = None
    errors: list[str] = []

    @staticmethod
    def from_response(base_response: BaseResponse[T]) -> "GenericResponse[T]":
        return GenericResponse[T](
            success=base_response.is_success,
            message=base_response.message,
            data=base_response.data,
            errors=base_response.errors,
        )

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "errors": self.errors,
        }
