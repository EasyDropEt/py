from typing import Annotated, Callable

from pika import ConnectionParameters, URLParameters, spec
from pika.adapters import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

Callback = Annotated[
    Callable[[BlockingChannel, spec.Basic.Deliver, spec.BasicProperties, bytes], None],
    "A callback function that receives a message from the queue.",
]


class RabbitMQSubscriber:
    def __init__(self, queue: str, callback: Callback) -> None:
        self._queue = queue
        self._callback = callback
        self._connection = self._connect_with_url_parameters(
            "amqps://khlfoide:YGxrgwG8NITXiFRzZ2kX8v0Tx_wAPJ0V@sparrow.rmq.cloudamqp.com/khlfoide",
        )

    def start(self) -> None:
        print("Starting subscriber...")
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue, durable=True)

        self._channel.basic_consume(
            queue=self._queue, on_message_callback=self._callback, auto_ack=True
        )
        self._channel.start_consuming()

    def stop(self) -> None:
        print("Stopping subscriber")
        self._connection.close()

    def _connect_with_connection_parameters(
        self, host: str, port: int
    ) -> BlockingConnection:
        connection_parameters = ConnectionParameters(host, port)
        return BlockingConnection(connection_parameters)

    def _connect_with_url_parameters(self, url: str) -> BlockingConnection:
        connection_parameters = URLParameters(url)
        return BlockingConnection(connection_parameters)


def example_callback(
    channel: BlockingChannel,
    method: spec.Basic.Deliver,
    properties: spec.BasicProperties,
    body: bytes,
) -> None:
    print(f" [x] Received '{str(body)}'")
