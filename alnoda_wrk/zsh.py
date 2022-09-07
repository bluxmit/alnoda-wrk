import os 
from .fileops import *
from .globals import *

VAR_ADMIN_TAG = " #<-- added by admin (variable)"
ALIAS_ADMIN_TAG = " #<-- added by admin (alias)"

def get_user_env_vars():
    """ ->> {}
    Get list of user's (zsh) env variables from ~/.zshrc 

    :return: dict of env variables name:value
    :rtype: dict
    """
    zshrc_lines = read_zshrc()
    env_vars = {}
    for line in zshrc_lines:
        if VAR_ADMIN_TAG in line:
            line_ = line.replace(VAR_ADMIN_TAG,"")
            line_ = line_.replace("export","")
            line_ = line_.strip()
            evl = line_.split("=")
            var_name = evl[0]
            var_val = evl[1]
            env_vars[var_name] = var_val
    return env_vars


def add_user_env_var(name, value):
    """ str, str ->>

    Add user env variable to the ~/.zshrc file
    :param name: env variable name 
    :type name: str
    :param value: env variable value 
    :type value: str
    """
    name = name.strip()
    evar = f'export {name}="{value}"'
    varline=f"\n{evar} {VAR_ADMIN_TAG}"
    add_zshrc_line(varline)
    return


def remove_user_env_var(name):
    """ str ->> 
    Remove user env variable from the ~/.zshrc file 
    :param name: user env variable name 
    :type name: str
    """
    zshrc_lines = read_zshrc()
    new_zshrc_lines = []
    for line in zshrc_lines:
        if VAR_ADMIN_TAG in line:
            if name in line:
                continue 
        new_zshrc_lines.append(line)
    # overwrite ~/.zshrc file 
    overwrite_zshrc(new_zshrc_lines)
    return


def get_user_aliases():
    """ ->> {}
    Get list of user's (zsh) aliases from ~/.zshrc 

    :return: dict of aliases name:value
    :rtype: dict
    """
    zshrc_lines = read_zshrc()
    aliases = {}
    for line in zshrc_lines:
        if ALIAS_ADMIN_TAG in line:
            line_ = line.replace(ALIAS_ADMIN_TAG,"")
            line_ = line_.replace("alias","")
            line_ = line_.strip()
            evl = line_.split("=")
            var_name = evl[0]
            var_val = evl[1]
            aliases[var_name] = var_val
    return aliases


def add_user_alias(name, cmd):
    """ str, str ->>

    Add user alias to the ~/.zshrc file
    :param name: alias short name 
    :type name: str
    :param cmd: alias command 
    :type cmd: str
    """
    name = name.strip()
    evar = f'alias {name}="{cmd}"'
    aliasline=f"\n{evar} {ALIAS_ADMIN_TAG}"
    add_zshrc_line(aliasline)
    return


def remove_user_alias(name):
    """ str ->> 
    Remove user alias from the ~/.zshrc file 
    :param name: user alias name 
    :type name: str
    """
    zshrc_lines = read_zshrc()
    new_zshrc_lines = []
    for line in zshrc_lines:
        if ALIAS_ADMIN_TAG in line:
            if name in line:
                continue 
        new_zshrc_lines.append(line)
    # overwrite ~/.zshrc file 
    overwrite_zshrc(new_zshrc_lines)
    return