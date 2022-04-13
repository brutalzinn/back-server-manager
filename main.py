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
# CPU_CORE = psutil.cpu_count()

@socketio.on('my event', namespace='/test')
def handle_my_custom_namespace_event(json):
    print('received json: ' + str(json))

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        count += 1
        mem_usage = psutil.virtual_memory()
        total_mem = bytes2human(mem_usage.total)
        used_mem = bytes2human(psutil.virtual_memory().total - psutil.virtual_memory().available)
        disk_percent = psutil.disk_usage('/').percent
        cpu_percent = psutil.cpu_percent(interval=0.5)
        cpu_frequency = psutil.cpu_freq().current

        teste = Data(os.getenv('ORIGIN'))

        teste.cpu_frequency = cpu_frequency
        teste.cpu_percent = cpu_percent

        teste.memory_used = used_mem
        teste.total_mem = total_mem
        teste.disk_percent = disk_percent

        socketio.emit('data', teste.to_dict())
        socketio.sleep(5)

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
    socketio.run(app,debug=True, host=os.getenv('HOST'),port=os.getenv('FLASK_PORT'))