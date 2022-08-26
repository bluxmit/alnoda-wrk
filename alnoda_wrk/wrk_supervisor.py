"""
Module to manage apps started with supervisor 
"""
import os 
import logging
from jinja2 import Template
from .globals import *
from .templates import supervisord_template


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