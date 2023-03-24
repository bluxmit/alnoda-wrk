"""
Module to manage apps started with supervisor 
"""
import os 
import re
import time
import logging
import subprocess
from jinja2 import Template
from .globals import *
from .templates import supervisord_template
from .fileops import *


def init_supervisord():
    """ ->> bool
    Ensure folder for supervisord and for UI app logs exist

    :return: whether supervisord was successfully initialized
    :rtype: bool
    """
    logging.debug(f'Making sure folder {SUPERVISORD_FOLDER} for supervisord exists')
    try:
        Path(SUPERVISORD_FOLDER).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.warning(f"Could not create folder for supervisord {SUPERVISORD_FOLDER}. Something went wrong. Error: {e}")
        return False
    logging.debug(f'Making sure folder {VAR_LOG_FOLDER} for app logs exists')
    try:
        Path(VAR_LOG_FOLDER).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.warning(f"Could not create folder for logs {VAR_LOG_FOLDER}. Something went wrong. Error: {e}")
        return False
    return True


def create_supervisord_file(name, cmd, folder=None, env_vars=None):
    """ str, str, str ->> 
    Add supervisord command and file to start an application

    :param name: name of the application
    :type name: str
    :param cmd: shell command that starts an application
    :type cmd: str
    :param folder: folder in where application should be started
    :type folder: str
    :param env_vars: env var definitions, i.e. ["TERM=xterm", "EDITOR=mc"]
    :type env_vars: list
    """
    init_supervisord() # <- make sure folders exist
    # make sure name is safestring 
    name = safestring(name, length=35)
    params = {"name": name, "cmd": cmd}
    if folder: params["folder"] = folder
    if env_vars: params["env_vars"] = env_vars
    tm = Template(supervisord_template)
    supervisord_file = tm.render(params)
    # write file to the supervisord folder
    supervisor_file = os.path.join(SUPERVISORD_FOLDER, f"{name}.conf")
    with open(supervisor_file, "w") as _file:
        _file.write(supervisord_file)
    logging.debug(f"creating startup for {name}")
    return


def get_app_command(name):
    """ str ->> str
    Opens supervisord file, and extracts the start command

    :param name: name of the application
    :type name: str
    :return: was it succesfull? 
    :rtype: bool
    """
    supervisord_file = name+".conf"
    with open(os.path.join(SUPERVISORD_FOLDER, supervisord_file)) as f:
        sd_lines = f.readlines()
    for line in sd_lines:
        if "command=/bin/sh -c \"" in line:
            r = re.search('command=/bin/sh -c "(.*)"', line)
            cmd = r.group(1)
    cmd = cmd.strip()
    return cmd


def get_started_apps(exclude=True):
    """ ->> [str]
    Return the list of supervisord files

    :return: list of app names
    :rtype: list[str]
    """
    excluded = ['supervisord', 'unified-supervisord', 'mkdocs']
    files = os.listdir(SUPERVISORD_FOLDER)
    lapps = [ap.replace(".conf","") for ap in files]
    # Create return dict of app and command
    apps = {}
    for app in lapps:
        if app not in excluded:
            apps[app] = get_app_command(app)
    return apps


def get_service_pids(cmd):
    """ str ->> [int]
    Gets pids of the process, started by a command cmd

    :param cmd: command used to start applicatio
    :type name: str
    :return: list of system pids to kill
    :rtype: list
    """
    ret_pids = set()
    cmd_ = cmd.replace(" &!", "").replace("&!", "").replace("&", "")
    # General case
    scmd_ = f"""ps aux | grep "{cmd_}" | sed 's/\s\s*/ /g' | cut -d' ' -f2"""
    stream = os.popen(scmd_)
    output = stream.read()
    pids = output.split("\n")
    for pid in pids:
        if pid is not None and pid != "" and pid.isnumeric(): 
            ret_pids.add(pid)
    return ret_pids


def stop_app(name: str):
    """ str, str ->> 
    Remove the supervisord file for the app

    :param name: name of the application
    :type name: str
    """
    supervisord_file = name+".conf"
    # delete supervisord file
    try:    os.remove(os.path.join(SUPERVISORD_FOLDER, supervisord_file))
    except: pass
    # also delete log files
    try:    os.remove(os.path.join(VAR_LOG_FOLDER, f"{choice}-stdout.log"))
    except: pass
    try:    os.remove(os.path.join(VAR_LOG_FOLDER, f"{choice}-stderr.log"))
    except: pass
    return 