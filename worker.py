# https://stackoverflow.com/questions/44371041/python-socketio-and-flask-how-to-stop-a-loop-in-a-background-thread
import uuid

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

    def __init__(self, socket_channel,socket_id, socketio):
        """
        assign socketio object to emit
        """
        self.socket_id = socket_id
        self.unique_id = str(uuid.uuid4())
        self.socket_channel = socket_channel
        self.socketio = socketio
        self.switch = True
        
    @threaded
    def do_work(self, method, *argv):
        """
        do work and emit message
        """
        print(self.switch)
        while self.switch:
            self.unit_of_work += 1
            method(self.socketio, argv)
            self.socketio.sleep(3)

    def stop(self):
        """
        stop the loop
        """
        print("Parando thread para "+ str(self.unit_of_work) + "--ID:--" + self.unique_id)
        self.switch = False