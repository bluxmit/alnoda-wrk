#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import atexit
import time
import json
import typer
import re
import ipaddress
from urllib.parse import urlparse
from .fileops import read_ui_conf
from .meta_about import read_meta
from .globals import * 


def is_hostname(s):
    """ Check if string looks like a proper host name"""
    if len(s) > 255:
        return False
    if s[-1] == ".":
        s = s[:-1]
    allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in s.split("."))


def is_ip(s):
    try:
        ipaddress.ip_address(s)
        return True
    except ValueError:
        return False


def is_url(s):
    try:
        result = urlparse(s)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def check_valid_host(s):
    """ Check if app input host is either valid hostname, ip or url"""
    if is_hostname(s): return True, 'hostname'
    if is_ip(s): return True, 'ip'
    if is_url(s): return True, 'url'
    return False, f'{s} is neither valid host name, nor IP or URL'


def is_port_in_app_use(port):
    """ Check if alnoda apps do not use this port """
    meta_dict = read_meta()
    if "alnoda.org.apps" not in meta_dict: return False
    for k,v in meta_dict['alnoda.org.apps'].items():
        if "app_port" in v: 
            try:
                if int(v['app_port']) == int(port): return True
            except: pass
    return False


def is_os_port_in_use(port):
    """ Simply check if port is not used by other running processes (irrelevant during docker build) """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('0.0.0.0', port)) == 0
    except:
        return False


def get_free_ports():
    """ Check if workspace has free ports, and return one of them """
    ui_conf = read_ui_conf()
    # what ports are already taken:
    taken_ports = []
    for page in ui_conf.keys():
        page_data = ui_conf[page]
        for app,adic in page_data.items():
            if 'port' in adic: taken_ports.append(adic['port'])
    # determine free ports
    free_ports = []
    for p in range(ALLOWED_FREE_PORT_RANGE_MIN, ALLOWED_FREE_PORT_RANGE_MAX+1):
        if p not in taken_ports:
            if not is_os_port_in_use(p):
                free_ports.append(p)
    return free_ports


def check_port_and_assign_target(port, source_check=True):
    """ Check if port is available, and find the port to map to """
    # check port is even valid
    if source_check:
        try: port = int(port)
        except: 
            return None, 'port must be a number'
        if port <= 0 or port >= 65535: 
            return None, 'port must be in range [0, 65535]'
        # first check original port is not in use 
        if is_port_in_app_use(port) or is_os_port_in_use(port):
            return None, 'port is already used'
    if port in WRK_RESERVED_PORTS: return port, ""
    free_ports = get_free_ports()
    if len(free_ports) == 0: return None, 'Reached limits of applications with UI'
    else:
        prescribed_port = free_ports[0]
        if port in free_ports: prescribed_port = port
    return prescribed_port, ""


def make_port_forward_cmd(from_port_, to_port_, from_host = "0.0.0.0"):
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
    if len(from_parts) == 1:
        from_port = from_parts[0]
    elif len(from_parts) == 2:
        from_host = from_parts[0]
        from_port = from_parts[1]
    else:
        return False, f"Invalid input for the source. Use one of options: 1. host:port 2. port"
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
             