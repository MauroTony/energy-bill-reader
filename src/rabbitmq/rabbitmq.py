import os
import json
import pika as broker
from time import sleep
from typing import Callable
from config import get_config
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import (
    AMQPConnectionError,
    ConnectionClosedByBroker,
    ChannelClosedByBroker,
)


config = get_config()

class RabbitMq:
    def __init__(self, thread_number):
        self.__username = config.RABBITMQ_USER
        self.__password = config.RABBITMQ_PASS
        self.__host = config.RABBITMQ_HOST
        self.__port = config.RABBITMQ_PORT
        self.__channel = None
        self.__thread = thread_number

    @property
    def channel(self) -> BlockingChannel:
        return self.__channel

    def connect_to_broker(self) -> bool:
        credentials = broker.PlainCredentials(self.__username, self.__password)
        parameters = broker.ConnectionParameters(
            credentials=credentials,
            host=self.__host,
            port=int(self.__port),
            virtual_host="/",
            heartbeat=3600,
        )
        try:
            connection = broker.BlockingConnection(parameters=parameters)
            self.__channel = connection.channel()
            print(f"Thread: {self.__thread}, Connected to rabbitmq!")
        except (AMQPConnectionError, Exception) as e:
            print(f"Thread: {self.__thread}, except: {e}")
            print(f"Thread: {self.__thread}, Error connecting to rabbitmq, retrying in 5 seconds...")
            sleep(5)
            self.connect_to_broker()
        return True

    def insert_queue(
        self, queue: str, callback: Callable[[BlockingChannel, bytes, int], None]
    ) -> None:
        self.channel.queue_declare(queue, auto_delete=False)

        self.channel.basic_consume(
            queue=queue,
            on_message_callback=lambda c, m, o, b: callback(c, b, m.delivery_tag),
            auto_ack=False,
        )

    def start_broker(self):
        try:
            self.channel.start_consuming()
            print(f"Thread: {self.__thread}, Started consuming messages!")
        except (
            ConnectionClosedByBroker,
            AMQPConnectionError,
            ChannelClosedByBroker,
            Exception,
        ) as e:
            print(f"Thread: {self.__thread}, Exception: {e}")
            print(f"Thread: {self.__thread}, Connection closed by rabbitmq, retrying in 5 seconds...")
            sleep(5)
            self.connect_to_broker()
            self.start_broker()

    def publish_in_queue(self, queue: str, data: dict, exchange: str = "") -> None:
        self.channel.basic_publish(
            exchange=exchange, routing_key=queue, body=json.dumps(data)
        )

    def close(self):
        self.__channel.close()
