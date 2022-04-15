import json
import os
import time
import psutil
from psutil._common import bytes2human
from models.stats_model import Data

def find_procs_by_name(name :str):
    "Return a list of processes matching 'name'."
    name = name.lower()
    ls = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
        if name in pinfo['name'].lower():
            pinfo['memory'] = bytes2human(proc.memory_info().vms)
            pinfo['memory_byte'] = proc.memory_info().vms
            ls.append(pinfo)
    ls = sorted(ls, key=lambda procObj: procObj['memory_byte'], reverse=True)
    return ls


def processes_thread(self, socketio, data):
    resultado = find_procs_by_name(data[0]['name'])
    print("PROCESS WORKER")
    
    socketio.emit('process_list', resultado, room=self.socket_id)
    
def background_thread(self, socketio, data):
    """Example of how to send server generated events to clients."""
    mem_usage = psutil.virtual_memory()
    total_mem = bytes2human(mem_usage[0])
    used_mem = bytes2human(mem_usage[3])
    disk_percent = psutil.disk_usage('/').percent
    cpu_percent = psutil.cpu_percent(interval=0.5)
    cpu_frequency = psutil.cpu_freq().current

    teste = Data(os.getenv('ORIGIN'))

    teste.cpu_frequency = cpu_frequency
    teste.cpu_percent = cpu_percent

    teste.memory_used = used_mem
    teste.total_mem = total_mem
    teste.disk_percent = disk_percent
    resultado = teste.to_dict()
    print("BACKGROUND WORKER")
    socketio.emit('stats_monitor', resultado, room=self.socket_id)
    