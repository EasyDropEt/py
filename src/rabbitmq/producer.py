import json

from pika.adapters import BlockingConnection
from pika.connection import ConnectionParameters, URLParameters


class RabbitMQProducer:
    def __init__(self, queue: str):
        self._queue = queue
        self._connection = self._connect_with_url_parameters(
            "amqps://khlfoide:YGxrgwG8NITXiFRzZ2kX8v0Tx_wAPJ0V@sparrow.rmq.cloudamqp.com/khlfoide",
        )

    def start(self) -> None:
        print("Starting producer")
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue, durable=True)

    def stop(self) -> None:
        print("Stopping producer...")
        self._connection.close()

    def publish(self, message: dict) -> None:
        assert "_channel" in self.__dict__, "Producer has not been started"
        self._channel.basic_publish(
            exchange="", routing_key=self._queue, body=json.dumps(message)
        )
        print(f" [x] Sent '{message}'")

    def _connect_with_connection_parameters(
        self, host: str, port: int
    ) -> BlockingConnection:
        connection_parameters = ConnectionParameters(host, port)
        return BlockingConnection(connection_parameters)

    def _connect_with_url_parameters(self, url: str) -> BlockingConnection:
        connection_parameters = URLParameters(url)
        return BlockingConnection(connection_parameters)
