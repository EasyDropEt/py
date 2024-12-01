import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from src.api_helpers import GenericResponse
from src.exception_helpers import ApplicationException
from src.logging_helpers import get_logger
from src.typing.config import TestRequestDto, TestResponseDto

LOG = get_logger()


class APIRequestHandler:
    def __init__(self) -> None:
        self._app = FastAPI()

        self._app.add_api_route(
            "/test",
            self._read_root,
            response_model=TestResponseDto,
        )

    def start(self) -> None:
        LOG.info("Starting api...")
        self._contain_exceptions()
        uvicorn.run(self._app, host="0.0.0.0", port=8000)

    def stop(self) -> None:
        LOG.info("API does not need to be stopped...")

    def _read_root(self, request_dto: TestRequestDto) -> TestResponseDto:
        LOG.info(request_dto)
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
