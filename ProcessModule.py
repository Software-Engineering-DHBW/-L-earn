"""
This file includes all functions, that are needed to get processes and their information for all operating systems and
handle operations on processes such as kill() in the future.
"""

import os
import platform
from datetime import datetime, date

import numpy as np
import pandas as pd
# import all necessary libraries and packages
import psutil

if platform.system() == "Windows":
    import win32gui
    import win32process

import wmctrl

import Exceptions

consideredProc = []

def filterProcLin(df):
    for win in wmctrl.Window.list():
        consideredProc.append(psutil.Process(win.pid).name())

#wmctrl.Window.get_active()
def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        consideredProc.append(psutil.Process(win32process.GetWindowThreadProcessId(hwnd)[1]).name())


def filterProcWin(df):
    win32gui.EnumWindows(winEnumHandler, None)
    for index, row in df.iterrows():
        if row["name"] not in consideredProc:
            df.drop(index, inplace=True)


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
            except (psutil.AccessDenied, psutil.ZombieProcess, psutil.NoSuchProcess):
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

            # append process with information to process list
            processes.append({
                'pid': pid, 'name': name, 'create_time': create_time, 'runtime': runtime.total_seconds(),
                'date': date.today()
            })

    # return process list
    return processes


def checkSystemProcess(name):
    sysWin = ['alg.exe', 'csrss.exe', 'ctfmon.exe', 'explorer.exe', 'lsass.exe', 'services.exe', 'smss.exe',
              'spoolsv.exe', 'svchost.exe', 'ntoskrnl.exe', 'winlogon.exe', 'System']

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

    if platform.system() == "Windows":
        filterProcWin(df)
    elif platform.system() == "Linux":
        filterProcWin(df)
    return df


class ProcessData(object):
    class __ProcessData:
        def __init__(self, bannedProcesses=[]):
            self.data = getAllProcesses()
            self.bannedProcesses = bannedProcesses

        def updateData(self):
            self.data = getAllProcesses()

        def checkProcesses(self):
            processes = self.data['name']
            running = []
            proc = set(processes)
            for b in self.banned:
                for p in proc:
                    if b in p:
                        running.append(b)

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

    instance = None

    def __new__(cls, *args, **kwargs):
        if not ProcessData.instance:
            ProcessData.instance = ProcessData.__ProcessData()
        return ProcessData.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
