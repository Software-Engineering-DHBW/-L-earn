import psutil
from datetime import datetime
import pandas as pd
import time
import os
import numpy as np

def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

def get_processes_info():
    # the list the contain all process dictionaries
    processes = []
    for process in psutil.process_iter():
        # get all process info in one shot
        with process.oneshot():
            # get the process id
            pid = process.pid

            #if pid == 0:
                # System Idle Process for Windows NT, useless to see anyways
                #continue
            name = process.name()
            try:
                create_time = datetime.fromtimestamp(process.create_time())
            except OSError:
                # system processes, using boot time instead
                create_time = datetime.fromtimestamp(psutil.boot_time())
            try:
                # get the number of CPU cores that can execute this process
                cores = len(process.cpu_affinity())
            except psutil.AccessDenied:
                cores = 0
                # get the CPU usage percentage
            cpu_usage = process.cpu_percent()

            # get the status of the process (running, idle, etc.)
            status = process.status()

            try:
                # get the process priority (a lower value means a more prioritized process)
                nice = int(process.nice())
            except psutil.AccessDenied:
                nice = 0

            try:
                # get the memory usage in bytes
                memory_usage = process.memory_full_info().uss
            except psutil.AccessDenied:
                memory_usage = 0

            # total process read and written bytes
            io_counters = process.io_counters()
            read_bytes = io_counters.read_bytes
            write_bytes = io_counters.write_bytes

            # get the number of total threads spawned by this process
            n_threads = process.num_threads()

            # get the username of user spawned the process
            try:
                username = process.username()
            except psutil.AccessDenied:
                username = "N/A"

            processes.append({
                'pid': pid, 'name': name, 'create_time': create_time,
                'cores': cores, 'cpu_usage': cpu_usage, 'status': status, 'nice': nice,
                'memory_usage': memory_usage, 'read_bytes': read_bytes, 'write_bytes': write_bytes,
                'n_threads': n_threads, 'username': username,
            })

    return processes

def construct_dataframe(processes):
    # convert to pandas dataframe
    df = pd.DataFrame(processes)
    # set the process id as index of a process
    df.set_index('pid', inplace=True)
    # sort rows by the column passed as argument
    df.sort_values(by='pid', inplace=True)
    # pretty printing bytes
    df['memory_usage'] = df['memory_usage'].apply(get_size)
    df['write_bytes'] = df['write_bytes'].apply(get_size)
    df['read_bytes'] = df['read_bytes'].apply(get_size)
    # convert to proper date format
    df['create_time'] = df['create_time'].apply(datetime.strftime, args=("%Y-%m-%d %H:%M:%S",))
    # reorder and define used columns
    #df = df[columns.split(",")]
    return df

if __name__ == "__main__":
    processes = get_processes_info()
    df = construct_dataframe(processes)
    print(df.to_string())
    data = df.loc[df['name'] == "msedge.exe"]
    print(data.to_string())
    for i in data.index:
        p = psutil.Process(i)
        p.kill()

def getAllProcesses():
    processes = get_processes_info()
    df = construct_dataframe(processes)
    return df


