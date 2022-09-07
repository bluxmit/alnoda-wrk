import os 
from .fileops import *
from .globals import *

ADMIN_TAG = "#<-- added by admin"

def get_user_env_vars():
    """ ->> {}
    Get list of user's (zsh) env variables from ~/.zshrc 

    :return: dict of env variables name:value
    :rtype: dict
    """
    zshrc_lines = read_zshrc()
    env_vars = {}
    for line in zshrc_lines:
        if ADMIN_TAG in line:
            ev_ = line.split(ADMIN_TAG)[0]
            evl = ev_.split("=")
            env_vars[evl[0]] = env_vars[evl[1]]  
    return env_vars


def add_user_env_var(name, value):
    """ str, str ->>

    Add user env (zsh) variable to the ~/.zshrc file
    :param name: env variable name 
    :type name: str
    :param value: env variable value 
    :type value: str
    """
    varline = f'export {name}="{value}"'
    add_zshrc_line(varline)
    return


def remove_user_env_var(name, value):
    """ str ->> 
    Remove user env variable from the ~/.zshrc file 
    :param name: user env variable name 
    :type name: str
    """
    zshrc_lines = read_zshrc
    new_zshrc_lines = []
    for line in zshrc_lines:
        if ADMIN_TAG in line:
            if name not in line:
                continue
        new_zshrc_lines.append(line)
    # overwrite ~/.zshrc file 
    overwrite_zshrc(new_zshrc_lines)
    return


