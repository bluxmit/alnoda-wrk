#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import atexit
import time
import json
import typer

from .globals import *

def kill_process(p):
    try:
        p.kill()  # This sends a SIGKILL, which cannot be caught or ignored
    except ProcessLookupError:
        pass  # Process might have already terminated


def make_port_forward_cmd(from_port_, to_port_):
    """ int/str, int/str ->>
    Check validity of inputs and create command to forward traffic. 
    
    :param from_port_: port or host:port to route from
    :type from_port_: int or str
    :param to_port_: port route to
    :type to_port_: int or str

    return success, command or error message
    """
    from_port_str = str(from_port_)
    to_port = str(to_port_)
    # if from_port_ has host, split it
    from_parts = from_port_str.split(':')
    from_host = "localhost"
    if len(from_parts) == 1:
        from_port = from_parts[0]
    elif len(from_parts) == 2:
        from_host = from_parts[0]
        from_port = from_parts[1]
    else:
        return False, f"Invalid input for the source. Use one of options: 1. host:port 2. port"
    # check ports are indeed correct 
    # ...
    # create traffic forwarding command
    fwd_cmd = f'socat tcp-listen:{to_port},reuseaddr,fork tcp:{from_host}:{from_port}'
    return True, fwd_cmd


def forward_port(from_port, to_port):
    """ int/str, int/str ->>
    :param from_port: port or host:port to route from
    :type from_port: int or str
    :param to_port: port route to
    :type to_port: int or str

    return process, message
    """
    success, cmd = make_port_forward_cmd(from_port, to_port)
    if not success:
        typer.echo(f"❗ {cmd}")
    else:
        typer.echo(cmd)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        # Register the kill function to be called on exit
        atexit.register(kill_process, process) 
        poll = process.poll()
        if poll is not None: 
            return None, "Failed to start forwarding traffic from [host:]port {from_port_} to localhost:{to_port_}"
        else:
            typer.echo("🔀 Start forwarding. Crl+c to terminate...")
            while True: 
                time.sleep(1)
             
        








'''
#### PM2 Processes are deprecated
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

'''