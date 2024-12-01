import uvicorn
from fastapi import FastAPI, Request, WebSocket
from starlette.responses import JSONResponse

from src.api_helpers import GenericResponse
from src.exception_helpers import ApplicationException
from src.logging_helpers import get_logger
from src.typing.config import TestRequestDto, TestResponseDto

LOG = get_logger()


class APIRequestHandler:
    def __init__(self) -> None:
        self._app = FastAPI()

        self._app.add_api_route("/test", self._rest)
        self._app.add_websocket_route("/ws", self._websocket)

    def start(self) -> None:
        LOG.info("Starting api...")
        self._contain_exceptions()
        uvicorn.run(self._app, host="0.0.0.0", port=8000)

    def stop(self) -> None:
        LOG.info("API does not need to be stopped...")

    async def _rest(self, request_dto: TestRequestDto) -> TestResponseDto:
        LOG.info(request_dto)
        return {"name": "World"}

    async def _websocket(self, websocket: WebSocket) -> None:
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")

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
