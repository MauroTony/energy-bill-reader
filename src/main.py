from config import get_config
from threading import Thread
from functions import Manager
from rabbitmq import RabbitMq

config = get_config()
class Application:
    @staticmethod
    def start_manager(thread_number):
        print(f'Starting manager, THREAD: {thread_number}')
        message_manager = Manager(RabbitMq(thread_number), thread_number)
        message_manager.start_messenger()

    def start(self):
        threads = config.THREADS
        for thread_number in range(0, threads):
            Thread(target=self.start_manager(thread_number)).start()

app = Application()
app.start()