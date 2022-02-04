import psutil
from datetime import datetime
import pandas as pd
import subprocess


# with command ps
def getProcesses():
    # the list the contain all process dictionaries
    processes = []

    ps = subprocess.Popen(['ps', 'auxc'], stdout=subprocess.PIPE).communicate()[0]
    pss = ps.splitlines(True)
    # this specifies the number of splits, so the splitted lines
    # will have (nfields+1) elements
    nfields = len(pss[0].split()) - 1
    for row in pss[1:]:
        process = row.decode('UTF-8').split(None, nfields)

        # get the process id
        pid = process[1]

        # get the name of the file executed
        name = process[10][:-1]

        # get the time the process was spawned
        create_time = process[8]

        # TIME (accumulated CPU time, user + system)
        cpu_time = process[9]

        # STAT (symbolic process state)
        state = process[7]

        # get the username of user spawned the process
        username = process[0]

        p = {
            'pid': pid, 'name': name,
            'create_time': create_time, 'cpu_time': cpu_time,
            'state': state, 'username': username,
        }
        processes.append(p)

        # print(p)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)
    df = pd.DataFrame(processes)
    print(df)

    return processes


# with psutil
def get_processes_info():
    # the list that contain all process dictionaries
    processes = []

    for process in psutil.process_iter():
        # get all process info in one shot
        with process.oneshot():
            # get the process id
            pid = process.pid
            if pid == 0:
                # System Idle Process for Windows NT, useless to see anyways
                continue

            try:
                # get the name of the file executed
                name = process.name()
            except psutil.ZombieProcess:
                continue

            # get the time the process was spawned
            try:
                create_time = datetime.fromtimestamp(process.create_time())
            except OSError:
                # system processes, using boot time instead
                create_time = datetime.fromtimestamp(psutil.boot_time())

            try:
                # get the number of CPU cores that can execute this process
                cores = len(process.cpu_affinity())
            except (psutil.AccessDenied, AttributeError) as e:
                cores = 0

            try:
                # get the CPU usage percentage
                cpu_usage = process.cpu_percent()
            except psutil.AccessDenied:
                cpu_usage = 0

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

            try:
                # total process read and written bytes
                io_counters = process.io_counters()
                read_bytes = io_counters.read_bytes
                write_bytes = io_counters.write_bytes
            except AttributeError:
                read_bytes = 0
                write_bytes = 0

            try:
                # get the number of total threads spawned by this process
                n_threads = process.num_threads()
            except psutil.AccessDenied:
                n_threads = 0

            # get the username of user spawned the process
            try:
                username = process.username()
            except psutil.AccessDenied:
                username = "N/A"

        p = {
            'pid': pid, 'name': name, 'create_time': create_time,
            'cores': cores, 'cpu_usage': cpu_usage, 'status': status, 'nice': nice,
            'memory_usage': memory_usage, 'read_bytes': read_bytes, 'write_bytes': write_bytes,
            'n_threads': n_threads, 'username': username,
        }
        processes.append(p)

        print(p)

    return processes
