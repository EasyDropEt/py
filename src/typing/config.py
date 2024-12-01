from typing import TypedDict


class Config(TypedDict): ...


class TestRequestDto(TypedDict):
    name: str


class TestResponseDto(TypedDict):
    name: str


class TestMessage(TypedDict):
    title: str
