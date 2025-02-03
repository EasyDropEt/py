from abc import ABCMeta, abstractmethod
from typing import Annotated, Callable, Generic, TypeVar

T = TypeVar("T")
CallbackFunction = Annotated[
    Callable[[T], None], "A callback function that receives a message from the queue."
]


class ABCSubscriber(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def start(self) -> None: ...

    @abstractmethod
    def stop(self) -> None: ...

    @abstractmethod
    def add_callback(self, callback_function: CallbackFunction) -> None: ...
