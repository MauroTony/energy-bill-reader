import json
import os
import time
import base64

from pika.adapters.blocking_connection import BlockingChannel
from .read_pdf import LeitorExtrato
from models import Result_final
from config import get_config

config = get_config()
class Manager:
    def __init__(self, broker, thread_number) -> None:
        self.__broker = broker
        self.thread_number = thread_number
        self.subscribe_queue = config.RABBITMQ_SUBSCRIBE_QUEUE

    def start_messenger(self):
        print(f"Starting messenger, THREAD: {self.thread_number}")
        self.__broker.connect_to_broker()

        self.__broker.insert_queue(self.subscribe_queue, self.callback_new_message)

        self.__broker.start_broker()

    @staticmethod
    def callback_new_message(
        channel: BlockingChannel, body: bytes, delivery_tag: int
    ) -> bool:
        timestamp = int(time.time())
        nome_arquivo = f"pdf_{timestamp}.pdf"
        try:
            data = json.loads(body)
            data = data["data"]
            pdf_base64 = data["pdfBase64"]
            id = data["Id"]
            print(f"Recebendo dados do id: {id}")

            pdf_content = base64.b64decode(pdf_base64)
            with open(nome_arquivo, "wb") as file:
                file.write(pdf_content)
            queue_name = config.RABBITMQ_PUBLISH_QUEUE

            leitor = LeitorExtrato(nome_arquivo)
            leitor.extrair_dados()
            content = {
                "pattern": "handle_extract",
                "data": leitor.dados
            }
            channel.basic_publish(
                exchange="", routing_key=queue_name, body=json.dumps(content)
            )
            channel.basic_ack(delivery_tag=delivery_tag)
            print(f"Enviando dados do Id:{id}")
        except Exception as e:
            print("Exception:", e)
        finally:
            try:
                os.remove(nome_arquivo)
            except Exception as e:
                print("Exception:", e)
        return True
