# https://stackoverflow.com/questions/44371041/python-socketio-and-flask-how-to-stop-a-loop-in-a-background-thread
import threading
import time
#gambiarra aproveitada do stackoverflow pra facilitar a implementação de multithread non blocking.
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class Worker(object):

    switch = False
    unit_of_work = 0

    def __init__(self, socketio):
        """
        assign socketio object to emit
        """
        self.socketio = socketio
        self.switch = True
        
    @threaded
    def do_work(self, method, *argv):
        """
        do work and emit message
        """
        while self.switch:
            self.unit_of_work += 1
            method(self.socketio, argv)
            time.sleep(3)

    def stop(self):
        """
        stop the loop
        """
        self.switch = False

    def start(self):
        """
        start the loop
        """
        self.switch = True