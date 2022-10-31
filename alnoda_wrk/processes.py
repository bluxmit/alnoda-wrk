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


def start_process(name, cmd, flags=""):
    """ str, str ->> 
    Start proces with PM2 

    :param name: process name
    :type name: str
    :param cmd: command that launches the process
    :type cmd: str
    :param flags: command additional flags
    :type cmd: str
    :return: list of pm2 processes
    :rtype: list
    """
    pm2_cmd = f'{PM2CMD} start {cmd} --name \"{name}\"'
    if len(flags) > 0:
        pm2_cmd = f"{pm2_cmd} -- {flags}"
    process = subprocess.Popen(pm2_cmd, shell=True, stdout=subprocess.PIPE)
    time.sleep(2)
    poll = process.poll()
    if poll is not None: 
        return False, "Failed"
    return True, "Started"

    

def stop_process(name):
    """ str ->> bool
    Stop pm2 process

    :param name: process name
    :type name: str
    """
    procs, pnames = get_processes()
    if name not in pnames:
        return False, "There is no process with this name"
    pm2_cmd = f'{PM2CMD} stop \"{name}\"'
    res = subprocess.check_output(pm2_cmd, shell=True, text=True)
    lres = res.splitlines()
    if lres[1].endswith("✓"):
        return True, ""
    else:
        return False, "Could not stop this process"

