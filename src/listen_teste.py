import pika
import pika as broker
import os
from dotenv import load_dotenv, find_dotenv
import json
load_dotenv(find_dotenv())
def escutar_fila_teste2():
    # Estabelece a conexão com o RabbitMQ
    credentials = broker.PlainCredentials(
        os.getenv("RABBITMQ_USER"), os.getenv("RABBITMQ_PASS")
    )
    parameters = broker.ConnectionParameters(
        credentials=credentials,
        host=os.getenv("RABBITMQ_HOST"),
        port=int(os.getenv("RABBITMQ_PORT")),
        virtual_host="/",
        heartbeat=3600
    )
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()

    # Declara a fila
    queue_name = 'UPREV_API_IMPORT_PDF_QUEUE'
    channel.queue_declare(queue=queue_name)

    # Função de callback para tratar as mensagens recebidas
    def callback(ch, method, properties, body):
        # Imprime o conteúdo do corpo (body) da mensagem
        print("Mensagem recebida:", json.loads(body.decode()) )

    # Registra a função de callback para receber as mensagens
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)

    # Inicia o consumo das mensagens
    channel.start_consuming()

# Exemplo de uso da função
escutar_fila_teste2()