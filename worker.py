# https://stackoverflow.com/questions/44371041/python-socketio-and-flask-how-to-stop-a-loop-in-a-background-thread
import uuid
from datetime import datetime

#gambiarra aproveitada do stackoverflow pra facilitar a implementação de multithread non blocking.


def threaded(fn):
    def wrapper(self, method, *argv):
        # thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        # thread.start()
        thread = self.socketio.start_background_task(target=lambda: fn(self, method, *argv))
        return thread
    return wrapper

class Worker(object):

    switch = False
    unit_of_work = 0
    socket_channel : str
    unique_id: str
    socket_id: str

    def __init__(self, socket_channel: str,socket_id :str, socketio):
        """
        assign socketio object to emit
        """
        self.socket_id = socket_id#.lower()
        self.unique_id = str(uuid.uuid4())
        self.socket_channel = socket_channel.lower()
        self.socketio = socketio
        self.switch = True
        data_atual = datetime.now()
        self.startAt  = data_atual.strftime('%d/%m/%Y %H:%M:%S')
        print(f'Crio thread Id: {self.unique_id} User: {self.socket_id} em {self.startAt}')

        
    @threaded
    def do_work(self, method, *argv):
        """
        do work and emit message
        """

        while True:
            if not self.switch: break
            self.unit_of_work += 1
            print(f"Thread iniciada em: {self.unique_id} - {self.startAt}")
            method(self, self.socketio, argv)
            self.socketio.sleep(3)
            

    def stop(self):
        """
        stop the loop
        """
        print(f'Parando thread para --ID: {self.unique_id} User: {self.socket_id}')
        self.switch = False

    def start(self):
        """
        start the loop
        """
        print(f'Iniciando thread para --ID: {self.unique_id} User: {self.socket_id}')
        self.switch = True