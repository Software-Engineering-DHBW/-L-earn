"""
This file includes all functions, that are needed to get processes and their information for all operating systems and
handle operations on processes such as kill() in the future.
"""

# import all necessary libraries and packages
import psutil
from datetime import datetime, date, timedelta
import time
import pandas as pd
import os, sys
import Exceptions
import numpy as np


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

            # Check if process is a system process
            if os.name == 'nt':
                if checkSystemProcess(process.name()):
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

            runtime = datetime.now() - create_time

            # get the status of the process (running, idle, etc.)
            try:
                status = process.status()
            except psutil.AccessDenied:
                status = "unknown"

            now = time.time()
            # append process with information to process list
            processes.append({
                'pid': pid, 'name': name, 'create_time': create_time, 'runtime': runtime.total_seconds()
            })

    # return process list
    return processes

def checkSystemProcess(name):
    sysWin = ['alg.exe', 'csrss.exe', 'ctfmon.exe', 'explorer.exe', 'lsass.exe', 'services.exe', 'smss.exe', 'spoolsv.exe', 'svchost.exe', 'ntoskrnl.exe', 'winlogon.exe', 'System']

    system = set(sysWin)
    # if os.name == 'nt':
    #    sys = set(sysWin)

    if name in system:
        return True


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
    #data = df.loc[df['name'] == "msedge.exe"]
    #print(data.to_string())

    # kill every Edge process
    #for i in data.index:
    #    p = psutil.Process(i)
    #    p.kill()

if __name__ == "__main__":
    processTest()

# Gives back the dataframe with all processes and information
def getAllProcesses():
    processes = get_processes_info()
    df = construct_dataframe(processes)
    return df

class ProcessData():
    def __init__(self, bannedProcesses=[]):
        self.data = getAllProcesses()
        self.bannedProcesses = bannedProcesses

    def updateData(self):
        self.data = getAllProcesses()

    def checkProcesses(self):
        processes = self.data[['name', 'runtime']]
        running = []
        proc = set(processes)
        for b in self.bannedProcesses:
            for p in proc:
                if b['limit'] != "NN":
                    if b['limit'] <= p['runtime']:
                        running.append(b)
                    else:
                        continue
                else:
                    if b in p['name']:
                        running.append(b)
                    else:
                        continue

        return running

    def setBannedProcesses(self, bp):
        if len(bp) != 0:
            self.bannedProcesses = bp
        else:
            raise Exceptions.EmptyValueError

    def clearBannedProcesses(self):
        self.bannedProcesses.clear()

    def getData(self):
        return self.data

    def getBannedProcesses(self):
        return self.bannedProcesses

    def extendBannedProcesses(self, name):
        if isinstance(name, (list, tuple, np.ndarray)):
            self.bannedProcesses.extend(name)
        else:
            self.bannedProcesses.append(name)

    def removeBannedProcess(self, name):
        if isinstance(name, (list, tuple, np.ndarray)):
            for n in name:
                try:
                    self.bannedProcesses.remove(n)
                except ValueError:
                    raise Exceptions.NotFoundError
        else:
            try:
                self.bannedProcesses.remove(name)
            except ValueError:
                raise Exceptions.NotFoundError

    def killProcess(self, name):
        print(name)
        if isinstance(name, (list, tuple, np.ndarray)):
            names = set(name)
            for n in names:
                df = set(self.data['name'])
                for d in df:
                    ds = set(d)
                    for s in ds:
                        if n in s:
                            p = psutil.Process(s['pid'])
                            p.kill()
        else:
            df = set(self.data.loc[name in self.data['name']])
            print(df)
            for d in df:
                #print(d)
                if name in d:
                    #print(d.index)
                    # p = psutil.Process(d['pid'])
                    # p.kill()
                    continue

if __name__ == "__main__":
    # processTest()
    pD = ProcessData(["msedge"])
    #print(pD.getData())
    print(pD.getBannedProcesses())
    pD.killProcess("msedge")