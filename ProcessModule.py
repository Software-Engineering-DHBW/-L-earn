"""
This file includes all functions, that are needed to get processes and their information for all operating systems and
handle operations on processes such as kill() in the future.
"""

# import all necessary libraries and packages
import psutil
from datetime import datetime
import pandas as pd


# Returns an array with all processes and their information
def get_processes_info():
    # the list that contains all process dictionaries
    processes = []
    for process in psutil.process_iter():
        # get all process info in one shot
        with process.oneshot():
            # get the process id
            try:
                pid = process.pid
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue

            # Skipping System Idle Process for Windows NT
            if pid == 0:
                continue

            # get process name
            try:
                name = process.name()
            except (psutil.AccessDenied, psutil.ZombieProcess):
                continue

            # get process create time
            try:
                create_time = datetime.fromtimestamp(process.create_time())
            except OSError:
                # system processes, using boot time instead
                create_time = datetime.fromtimestamp(psutil.boot_time())

            # get the status of the process (running, idle, etc.)
            try:
                status = process.status()
            except psutil.AccessDenied:
                status = "unknown"

            # append process with information to process list
            processes.append({
                'pid': pid, 'name': name, 'create_time': create_time
            })

    # return process list
    return processes


# Constructs a dataframe out of the process list array
def construct_dataframe(processes):
    # convert to pandas dataframe
    df = pd.DataFrame(processes)
    # set the process id as index of a process
    df.set_index('pid', inplace=True)
    # sort rows by process id
    df.sort_values(by='pid', inplace=True)
    # convert to proper date format
    df['create_time'] = df['create_time'].apply(datetime.strftime, args=("%Y-%m-%d %H:%M:%S",))
    return df


# First test function to try getting processes and killing them
def processTest():
    processes = get_processes_info()
    df = construct_dataframe(processes)

    print(df.to_string())

    # filter for all Edge processes
    data = df.loc[df['name'] == "msedge.exe"]
    print(data.to_string())

    # kill every Edge process
    for i in data.index:
        p = psutil.Process(i)
        p.kill()


# Gives back the dataframe with all processes and information
def getAllProcesses():
    processes = get_processes_info()
    df = construct_dataframe(processes)
    return df
