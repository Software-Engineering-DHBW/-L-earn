"""
This file includes all functions, that are needed to get processes and their information for all operating systems and
handle operations on processes.
"""
import os
import platform
import subprocess
import time
from datetime import datetime, date
from sys import platform

import numpy as np
import pandas as pd
import psutil

# import different packages for different OS
if platform == "win32":
    import win32gui
    import win32process
elif platform == "linux":
    import wmctrl

from classes import Exceptions

consideredProc = []

# Filter unnecessary processes for Linux, Mac, Windows
def filterProcMac(df):
    windowList = subprocess.check_output(["osascript -e 'tell application \"System Events\" "
                                          "to get the name of every process whose visible is true'"],
                                         shell=True).decode().replace("\n", "").split(", ")
    for i in range(len(windowList)):
        windowList[i] = windowList[i].lower()

    for index, row in df.iterrows():
        if row['name'] not in windowList:
            df.drop(index, inplace=True)


def filterProcLin(df):
    for win in wmctrl.Window.list():
        consideredProc.append(psutil.Process(win.pid).name().lower())
    for index, row in df.iterrows():
        if row["name"] not in consideredProc:
            df.drop(index, inplace=True)


# wmctrl.Window.get_active()
def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        consideredProc.append(psutil.Process(win32process.GetWindowThreadProcessId(hwnd)[1]).name().lower())


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


# Checks if a process is a system process
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
    df = pd.DataFrame(processes)
    df.set_index('pid', inplace=True)
    df.sort_values(by='pid', inplace=True)
    # convert to proper date format
    df['create_time'] = df['create_time'].apply(datetime.strftime, args=("%Y-%m-%d %H:%M:%S",))
    return df


# Gives back the dataframe with all processes and information
def getAllProcesses():
    processes = get_processes_info()
    df = construct_dataframe(processes)

    if platform == "linux" or platform == "linux2":
        # linux
        filterProcLin(df)
    elif platform == "darwin":
        # OS X
        filterProcMac(df)
    elif platform == "win32":
        # Windows...
        filterProcWin(df)
    return df

# singleton class with all processes, information and functions
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

                    # get limit
                    for index1, row1 in limits.iterrows():
                        limit = row1['limittime']

                    # cjeck if searched process is in data
                    if n.lower() in row['name']:
                        if limit != -1:
                            if limit <= row['runtime']:
                                if n.lower() in running:
                                    continue
                                else:
                                    running.append(n.lower())
                            else:
                                continue
                        else:
                            if n.lower() in running:
                                continue
                            else:
                                running.append(n.lower())
                    else:
                        continue

            return running

        def setBannedProcesses(self, bp):
            self.bannedProcesses = bp

        def clearBannedProcesses(self):
            self.bannedProcesses.clear()

        def getData(self):
            return self.data

        def getBannedProcesses(self):
            return self.bannedProcesses.copy()

        # add new processes to bannedProcesses
        def extendBannedProcesses(self, banned):
            if len(self.bannedProcesses) == 0:
                self.bannedProcesses = banned
            else:
                for index, name in banned.iterrows():
                    for ind, bn in self.bannedProcesses.iterrows():
                        # check if process is already in banned processes and if so drop existing entry
                        if name['name'].lower() in bn['name'].lower():
                            self.bannedProcesses = self.bannedProcesses.drop(ind)
                self.bannedProcesses = pd.concat([self.bannedProcesses, banned])

        # remove one specific banned process
        def removeBannedProcess(self, name):
            for ind, row in self.bannedProcesses.iterrows():
                if name in row['name']:
                    self.bannedProcesses.drop(ind)

        def killProcess(self, name):
            if len(name) == 0:
                raise Exceptions.EmptyValueError
            else:
                # check if name is an array
                if isinstance(name, (list, tuple, np.ndarray)):
                    names = set(name)
                    df = set(self.data['name'])
                    for n in names:
                        for d in df:
                            if n.lower() in d:
                                kill = self.data.loc[self.data["name"] == d]
                                for i in kill.index:
                                    try:
                                        proc = psutil.Process(i)
                                    except psutil.NoSuchProcess:
                                        continue
                                    try:
                                        proc.kill()
                                    except psutil.AccessDenied:
                                        continue

                else:
                    df = set(self.data['name'])
                    for n in df:
                        if name.lower() in n:
                            kill = self.data.loc[self.data["name"] == n]
                            for i in kill.index:
                                try:
                                    proc = psutil.Process(i)
                                except psutil.NoSuchProcess:
                                    continue
                                try:
                                    proc.kill()
                                except psutil.AccessDenied:
                                    continue

    # implementation of singleton pattern
    instance = None

    def __new__(cls, bannedProc=None, *args, **kwargs):
        if bannedProc is None:
            bannedProc = pd.DataFrame([])
        if not ProcessData.instance:
            ProcessData.instance = ProcessData.__ProcessData(bannedProc)
        return ProcessData.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)

