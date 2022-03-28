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
import subprocess


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
            #if os.name == 'nt':
            #    if checkSystemProcess(process.name()):
            #        continue

            # get process name
            try:
                name = process.name()
            except (psutil.AccessDenied, psutil.ZombieProcess, psutil.NoSuchProcess):
                continue

            # get process create time
            try:
                create_time = datetime.fromtimestamp(process.create_time())
            except OSError:
                # system processes, using boot time instead
                create_time = datetime.fromtimestamp(psutil.boot_time())

            runtime = (datetime.now() - create_time).total_seconds()

            # get the status of the process (running, idle, etc.)
            try:
                status = process.status()
            except psutil.AccessDenied:
                status = "unknown"

            now = time.time()
            if now < runtime:
                runtime = runtime - now

            # append process with information to process list
            processes.append({
                'pid': pid, 'name': name.lower(), 'create_time': create_time, 'runtime': runtime, 'date': date.today()
            })

    # return process list
    return processes

# Checks if a proces is a system process
def checkSystemProcess(name):
    #sysWin = ['alg.exe', 'csrss.exe', 'ctfmon.exe', 'explorer.exe', 'lsass.exe', 'services.exe', 'smss.exe', 'spoolsv.exe', 'svchost.exe', 'ntoskrnl.exe', 'winlogon.exe', 'System']

    #system = set(sysWin)
    # if os.name == 'nt':
    #    sys = set(sysWin)
    system = []

    # getting all processes that are opened through a window, which means they are no system process
    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select ProcessName'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if line.rstrip():
            system.append(line.decode().rstrip())

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
    # data = df.loc[df['name'] == "msedge.exe"]
    # print(data.to_string())

    # kill every Edge process
    # for i in data.index:
    #    p = psutil.Process(i)
    #    p.kill()


if __name__ == "__main__":
    processTest()


# Gives back the dataframe with all processes and information
def getAllProcesses():
    processes = get_processes_info()
    df = construct_dataframe(processes)
    return df


class ProcessData(object):
    class __ProcessData:
        def __init__(self, bannedProcesses):
            self.data = getAllProcesses()
            self.bannedProcesses = bannedProcesses

        def updateData(self):
            self.data = getAllProcesses()

        def checkProcesses(self):
            proc = self.data[['name', 'runtime']]
            running = []
            names = self.bannedProcesses["name"]
            for n in names:
                for index, row in proc.iterrows():
                    limits = self.bannedProcesses[self.bannedProcesses["name"] == n]
                    limit = -1

                    for index1, row1 in limits.iterrows():
                        limit = row1['limit']

                    if limit != -1:
                        if limit <= row['runtime']:
                            if n.lower() in running:
                                continue
                            else:
                                running.append(n.lower())
                        else:
                            continue
                    else:
                        if n.lower() in row['name']:
                            if n.lower() in running:
                                continue
                            else:
                                running.append(n.lower())
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
            if len(name) == 0:
                raise Exceptions.EmptyValueError
            else:
                if isinstance(name, (list, tuple, np.ndarray)):
                    names = set(name)
                    df = set(self.data['name'])
                    for n in names:
                        for d in df:
                            if n.lower() in d:
                                kill = self.data.loc[self.data["name"] == d]
                                for i in kill.index:
                                    proc = psutil.Process(i)
                                    proc.kill()

                else:
                    df = set(self.data['name'])
                    for n in df:
                        if name.lower() in n:
                            kill = self.data.loc[self.data["name"] == n]
                            for i in kill.index:
                                proc = psutil.Process(i)
                                try:
                                    proc.kill()
                                except psutil.AccessDenied:
                                    continue



    instance = None

    def __new__(cls, banned=None, *args, **kwargs):
        if banned is None:
            banned = []
        if not ProcessData.instance:
            ProcessData.instance = ProcessData.__ProcessData(banned)
        return ProcessData.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)



if __name__ == "__main__":
    # processTest()
    b = {'name': ["msegde", "Spotify", "chrome"], 'limit': [-1, -1, 500]}
    banned = pd.DataFrame(b)
    pD = ProcessData(banned)
    #print(pD.getData())
    print(pD.getBannedProcesses())
    # pD.killProcess("spotify")
    print(pD.checkProcesses())