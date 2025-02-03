from fastapi import APIRouter, Depends, WebSocket
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from src.application.features.some_feature.dtos.some_create_dto import SomeCreateDto
from src.application.features.some_feature.dtos.some_response_dto import SomeResponseDto
from src.application.features.some_feature.requests.commands.some_command import (
    SomeCommand,
)
from src.common.logging_helpers import get_logger
from src.webapi.common.helpers import GenericResponse, rest_endpoint
from src.webapi.dependency_setup import DependencySetup

LOG = get_logger()


class SomeFeatureController:
    def __init__(self) -> None:
        self._router = APIRouter(prefix="/some-feature", tags=["Some Feature"])

        self._register_routes()

    @property
    def router(self):
        return self._router

    def _register_routes(self) -> None:
        self._router.get("/get", response_model=GenericResponse[SomeResponseDto])(
            self.get
        )
        self._router.post("/post", response_model=GenericResponse[SomeResponseDto])(
            self.post
        )
        self._router.websocket("/ws")(self.websocket)

    @rest_endpoint
    async def get(
        self, mediator: Annotated[Mediator, Depends(DependencySetup.get_mediator)]
    ):
        LOG.info("Satisfying request")
        return await mediator.send(SomeCommand(dto=SomeCreateDto("Message")))

    @rest_endpoint
    async def post(
        self,
        request_dto: SomeCreateDto,
        mediator: Annotated[Mediator, Depends(DependencySetup.get_mediator)],
    ):
        LOG.info(f"Satisfying request {request_dto}")
        return await mediator.send(SomeCommand(dto=request_dto))

    async def websocket(self, ws: WebSocket) -> None:
        await ws.accept()

        while True:
            data = await ws.receive_text()
            await ws.send_text(f"Message text was: {data}")
