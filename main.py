import json
import time
import psutil
import os
from threading import Lock
from flask import Flask, request
from flask_socketio import SocketIO, disconnect
from psutil._common import bytes2human
from models.stats_model import Data
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger=True)
thread = None
thread_lock = Lock()


@socketio.on('my event', namespace='/test')
def handle_my_custom_namespace_event(json):
    print('received json: ' + str(json))


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        count += 1
        mem_usage = psutil.virtual_memory()
        total_mem = bytes2human(mem_usage[0])
        used_mem = bytes2human(mem_usage[3])
        disk_percent = psutil.disk_usage('/').percent
        cpu_percent = psutil.cpu_percent(interval=None)

        teste = Data("Notebook")
        teste.memory_used = used_mem
        teste.total_mem = total_mem
        teste.disk_percent = disk_percent
        teste.cpu_percent = cpu_percent

        socketio.emit('data', teste.to_dict())
        socketio.sleep(10)

# @socketio.on('disconnect')
# def disconnect():
#     print('client disconnected',request.sid)

@socketio.on('connect')
def connect():
    global thread
    if "Api-Key" not in request.headers or request.headers.get('Api-Key') != os.getenv('API_KEY'):
        disconnect()
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    
if __name__ == '__main__':
    socketio.run(app,debug=True,host="0.0.0.0", port=8888)