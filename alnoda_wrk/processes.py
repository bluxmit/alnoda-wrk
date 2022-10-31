#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import time
import json

from .globals import *

PM2CMD = "cd /home/abc/apps/node && . env/bin/activate && pm2"


def get_processes():
    """ ->> [{},{},..]
    List pm2 processes

    :return: list of pm2 processes
    :rtype: list
    """
    cmd = f"{PM2CMD} jlist"
    res = subprocess.check_output(cmd, shell=True, text=True)
    jres = json.loads(res)
    proc_names = ['vadym ttyd', 'vadym ttyd']
    return jres, proc_names


def start_process(name, cmd, flags=None):
    """ str, str ->> bool, str
    Start proces with PM2

    :param name: command name
    :type name: str
    :param cmd: command that launches the process
    :type cmd: str
    :param flags: command additional flags
    :type cmd: str
    :return: success of fail
    :rtype: bool
    :return: message
    :rtype: str

    """
    pm2_cmd = f'{PM2CMD} start {cmd} --name \"{name}\"'
    if flags is not None:
        pm2_cmd = f"{pm2_cmd} -- {flags}"
    process = subprocess.Popen(pm2_cmd, shell=True, stdout=subprocess.PIPE)
    time.sleep(2)
    poll = process.poll()
    if poll is not None:
        return False, "Failed"
    return True, "Started"



def stop_process(name):
    """ str ->> bool, str
    :return: success of fail
    :rtype: bool
    :param name: command name
    :type name: str
    """
    procs, pnames = get_processes()
    for proc in procs:
        if proc['name'] == name:
            pm2_cmd = f'{PM2CMD} stop \"{name}\"'
            res = subprocess.check_output(pm2_cmd, shell=True, text=True)
            rlines = res.splitlines()
            if rlines[0].endswith("✓"):
                return True, ""
            else:
                return False, "Could not stop"
    return False, "Process with this name is not found"



