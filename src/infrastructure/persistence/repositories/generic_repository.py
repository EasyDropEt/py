from typing import Any, TypeVar
from uuid import UUID

from src.application.contracts.abc_generic_repository import ABCGenericRepository
from src.infrastructure.persistence.helpers import repository_class

T = TypeVar("T")


@repository_class
class GenericRepository(ABCGenericRepository[T]):
    def get_all(self, **filters: Any) -> list[T]: ...

    def get(self, **filters: Any) -> T: ...

    def create(self, entity: T) -> T: ...

    def update(self, id: UUID, entity: T) -> bool: ...

    def delete(self, id: UUID) -> bool: ...
