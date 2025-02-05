from typing import Annotated

from fastapi import Depends
from rmediator.mediator import Mediator

from src.application.contracts.infrastructure.message_queue.abc_producer import (
    ABCProducer,
)
from src.application.contracts.infrastructure.message_queue.abc_subscriber import (
    ABCSubscriber,
)
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.common.generic_helpers import get_config
from src.common.singleton_helpers import SingletonMeta
from src.common.typing.config import Config, TestMessage
from src.infrastructure.persistence.db_client import DbClient
from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.infrastructure.rabbitmq.producer import RabbitMQProducer
from src.infrastructure.rabbitmq.subscriber import RabbitMQSubscriber


class DependencySetup(metaclass=SingletonMeta):
    @staticmethod
    def get_db_client(config: Annotated[Config, Depends(get_config)]) -> DbClient:
        return DbClient(
            config["mongo_db_connection_string"],
            config["db_name"],
        )

    @staticmethod
    def get_uow(
        db_client: Annotated[DbClient, Depends(get_db_client)]
    ) -> ABCUnitOfWork:
        return UnitOfWork(db_client)

    @staticmethod
    def get_producer(config: Annotated[Config, Depends(get_config)]) -> ABCProducer:
        producer = RabbitMQProducer[TestMessage](
            config["rabbitmq_url"],
            config["rabbitmq_queue"],
        )
        producer.start()

        return producer

    @staticmethod
    def get_subscriber(config: Annotated[Config, Depends(get_config)]) -> ABCSubscriber:
        subscriber = RabbitMQSubscriber[TestMessage](
            config["rabbitmq_url"],
            config["rabbitmq_queue"],
        )
        subscriber.start()

        return subscriber

    @staticmethod
    def get_mediator(
        uow: Annotated[ABCUnitOfWork, Depends(get_uow)],
        producer: Annotated[ABCProducer, Depends(get_producer)],
    ) -> Mediator:
        mediator = Mediator()

        handlers = []
        for command, handler in handlers:
            mediator.register_handler(command, handler)

        return mediator
