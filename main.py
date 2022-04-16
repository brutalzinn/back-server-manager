from ast import List
import json
import time
from tkinter import E
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
socketio = SocketIO(app, logger=False)
threads = []
psutil.PROCFS_PATH = '/rootfs/proc'
@socketio.on('connect')
def connect():

    if "Api-Key" not in request.headers or request.headers.get('Api-Key') != os.getenv('API_KEY'):
        print("sem api key.")
        socketio.emit("info", {"message":"Você não possui permissão para acessar esse servidor."})
        disconnect()
        return
        
    threads.append(Worker("server_process_list", request.sid, socketio))
    threads.append(Worker("server_stats", request.sid, socketio))

    print(f'Crio {len(threads)} threads para o ' + request.sid)


def checkThreadIsRunning(channel) -> bool:
    for w in threads:
        if w.socket_channel == channel and w.switch:
            return True
    return False

def killThreadByChannel(channel) -> bool:
    for w in threads:
        if w.socket_channel == channel:
            w.stop()

def getThreadByChannel(channel:str , socket_id: str) -> Worker:
    for w in threads:
        if w.socket_channel == channel.lower() and w.socket_id.lower() == socket_id.lower():
            return w

def removeThreads(channel, socket_id):
    removidas = 0
    for t in threads: 
        exist = t.channel == channel and socket_id.lower() == t.socket_id.lower()
        if exist : 
            removidas += 1
            # print("THREADS REMOVIDAS: " + str(removidas))
            t.stop()
            threads.remove(t)

def removeAllThreads(socket_id :str):
    print(f"Preparando para remover.. {len(threads)}")
    toRemove = []
    for t in threads: 
        exist = socket_id.lower() == t.socket_id.lower()
        if exist:
            t.stop()
            toRemove.append(t)
    for t in toRemove:
        print(f"Removendo. {t.unique_id}")
        threads.remove(t)      

def restartThreadByChannel(channel: str, socket_id: str):
    worker = getThreadByChannel(channel, socket_id)
    if worker.switch:
        worker.stop()
        worker = Worker(channel, socket_id, socketio)
        for i, n in enumerate(threads):
            if n.socket_channel == channel:
                threads[i] = worker
    return worker

@socketio.on('disconnect')
def remove_user_threads():
    removeAllThreads(request.sid)
    print('client disconnected', request.sid)

@socketio.on('server_stats')
def server_status(json):
    print("server_stats")
    worker = restartThreadByChannel("server_stats", request.sid)
    worker.do_work(background_thread, json)

@socketio.on('server_process_list')
def process(json):
    print("server_process_list")
    worker = restartThreadByChannel("server_process_list", request.sid)
    worker.do_work(processes_thread, json)


if __name__ == '__main__':
    socketio.run(app, debug=True, host=os.getenv('HOST') or "0.0.0.0",port=os.getenv('FLASK_PORT') or 5555)