from src.application.contracts.infrastructure.persistence.abc_some_repository import (
    ABCSomeEntityRepository,
)
from src.domain.entities.some_entity import SomeEntity
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.helpers import repository_class
from src.infrastructure.persistence.repositories.generic_repository import (
    GenericRepository,
)


@repository_class
class SomeEntityRepository(GenericRepository[SomeEntity], ABCSomeEntityRepository):
    def __init__(self, db_client: DbClient) -> None:
        super().__init__(db_client, "some_entity")
