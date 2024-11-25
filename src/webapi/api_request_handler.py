from typing import TypedDict

import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from src.api_helpers import GenericResponse
from src.exception_helpers import ApplicationException


class TestRequestDto(TypedDict):
    name: str


class TestResponseDto(TypedDict):
    name: str


class APIRequestHandler:
    def __init__(self) -> None:
        self._app = FastAPI()

        self._app.add_api_route("/test", self.read_root)

    def start(self) -> None:
        print("Starting api...")
        self._contain_exceptions()
        uvicorn.run(self._app, host="0.0.0.0", port=8000)

    def stop(self) -> None:
        print("API does not need to be stopped...")

    def read_root(self, request_dto: TestRequestDto) -> TestResponseDto:
        print(request_dto)
        return {"name": "World"}

    def _contain_exceptions(self) -> None:
        @self._app.exception_handler(ApplicationException)
        async def application_exception_handler(
            request: Request, exception: ApplicationException
        ) -> JSONResponse:
            return JSONResponse(
                status_code=exception.error_code,
                content=GenericResponse(
                    success=False,
                    message=exception.message,
                    errors=exception.errors,
                    data=None,
                ).to_dict(),
            )
