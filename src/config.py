import os
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel

load_dotenv(find_dotenv())

class GeneralConfig(BaseModel):
    # rabbitmq enviroments
    RABBITMQ_USER: str = os.getenv('RABBITMQ_USER')
    RABBITMQ_PASS: str = os.getenv('RABBITMQ_PASS')
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
    RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
    RABBITMQ_SUBSCRIBE_QUEUE = os.getenv('RABBITMQ_SUBSCRIBE_QUEUE')
    RABBITMQ_PUBLISH_QUEUE1 = os.getenv('RABBITMQ_PUBLISH_QUEUE1')
    RABBITMQ_PUBLISH_QUEUE2 = os.getenv('RABBITMQ_PUBLISH_QUEUE2')

    # config system enviroments
    THREADS = int(os.getenv('THREADS'))

def get_config() -> GeneralConfig:
    return GeneralConfig()