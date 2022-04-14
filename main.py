import json
import time
import psutil
import os
from threading import Lock
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, disconnect
from psutil._common import bytes2human
from models.stats_model import Data
from ps_utilities import background_thread, processes_thread
from worker import Worker
# gambiarra por agora. Até criar uma classe pra facilitar condição de sinal

app = Flask(__name__)
socketio = SocketIO(app, logger=True)

worker_processes = None
worker_stats = None

@socketio.on('disconnect')
def disconnect():
    global worker_processes, worker_stats
    if worker_processes != None : worker_processes.stop()
    if worker_stats != None : worker_stats.stop()
    print('Fecho a instância criada.')
    print('client disconnected',request.sid)

@socketio.on('connect')
def connect():
    print('Inicio a conexão com ',request.sid)
    # if "Api-Key" not in request.headers or request.headers.get('Api-Key') != os.getenv('API_KEY'):
    #     print("sem api key.")
    #     socketio.emit("info", {"message":"Você não possui permissão para acessar esse servidor."})
    #     disconnect()

@socketio.on('server_stats')
def server_status(json):
    global worker_stats
    worker_stats = Worker(socketio)
    print("inicio thread com hardware info e envio para o cliente")
    worker_stats.do_work(background_thread, json)

@socketio.on('server_process_list')
def process(json):
    global worker_processes
    worker_processes = Worker(socketio)
    print("inicio thread com uma lista de processos que pode ser filtrada por nome e por ordem de maior consumo de memória")
    print("Recebi no body request",str(json))
    worker_processes.do_work(processes_thread, json)

if __name__ == '__main__':
    socketio.run(app, debug=True, host=os.getenv('HOST'),port=os.getenv('FLASK_PORT'))