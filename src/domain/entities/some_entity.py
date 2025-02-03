from dataclasses import dataclass
from uuid import UUID


@dataclass
class SomeEntity:
    id: UUID
    name: str
    email: str
    age: int
