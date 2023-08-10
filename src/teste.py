import pika
import pika as broker
import os
from dotenv import load_dotenv, find_dotenv
import base64
import json

load_dotenv(find_dotenv())
def enviar_pdf_para_fila(pdf_path):
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
    queue_name = 'UPREV_READ_PDF_QUEUE'
    channel.queue_declare(queue=queue_name, auto_delete=False)

    # Lê o conteúdo do arquivo PDF
    with open(pdf_path, 'rb') as file:
        pdf_content = file.read()
    pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
    content = {
        "data": {
            "Id": "1",
            "pdfBase64": pdf_base64
        }
    }
    # Envia o conteúdo do PDF para a fila
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(content))

    # Fecha a conexão
    connection.close()

# Exemplo de uso da função
enviar_pdf_para_fila('pdfs/extrato(2).pdf')