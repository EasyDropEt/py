from typing import Annotated

from fastapi import Depends
from rmediator.mediator import Mediator

from src.application.features.user.handlers.commands.some_command_handler import (
    SomeCommandHandler,
)
from src.application.features.user.requests.commands.some_command import SomeCommand
from src.infrastructure.persistence.unit_of_work import UnitOfWork


def unit_of_work() -> UnitOfWork:
    return UnitOfWork()


def mediator(uow: Annotated[UnitOfWork, Depends(unit_of_work)]) -> Mediator:
    mediator = Mediator()

    # User use cases
    mediator.register_handler(SomeCommand, SomeCommandHandler(uow))

    return mediator
