import os 
import logging
import json, yaml
from jinja2 import Template
from collections import OrderedDict
from .globals import *
from .templates import cheatsheet_template

CHEATSHEET_DATA_FILE = os.path.join(WORKSPACE_DIR, 'cheatsheet.json') 
WORKSPACE_CHEATSHEET_FILE = os.path.join(WORKSPACE_UI_DIR, 'docs', 'cheatsheet.md')

def read_cheatsheet_data():
    """ ->> {}
    Reads existing cheatsheet data json file, and returns dict.

    :return: existing cheatsheet as dict
    :rtype: OrderedDict
    """
    if not os.path.exists(CHEATSHEET_DATA_FILE):
        with open(CHEATSHEET_DATA_FILE, "x") as f:
            f.write("{}")
    with open(CHEATSHEET_DATA_FILE) as json_file:
        cheatsheet_dict = json.load(json_file)
    return OrderedDict(cheatsheet_dict)

def write_cheatsheet_data(cheatsheet_dict):
    """ {} ->> 
    Overwrite existing cheatsheet json with the updated dict

    :param cheatsheet_dict: dict with the updated cheatsheet
    :type cheatsheet_dict: OrderedDict
    """
    with open(CHEATSHEET_DATA_FILE, 'w') as file:
        json.dump(cheatsheet_dict, file, indent=4 * ' ')
    return 

def refresh_cheatsheet_page():
    """ ->>
    Refreshes from sheatsheet dict worksapce page (in the .wrk)
    """
    # read cheatsheet json
    cheatsheet_dict = read_cheatsheet_data()
    # generate page from template
    tm = Template(cheatsheet_template)
    cheatsheet_page = tm.render(data=cheatsheet_dict)
    # overwrite cheatsheet.md page
    with open(WORKSPACE_CHEATSHEET_FILE, "w") as cheatsheet_md_file:
        cheatsheet_md_file.write(cheatsheet_page)
    return 
    
def add_cheatsheet_section(section):
    """ ->>
    Add new section (empty) to the cheatsheet_dict, 
    update the json file and refresh the .md page

    :param section: name of the new section
    :type section: str
    """
    # Add section in the beginning
    section_dict = OrderedDict([(section, {})])
    cheatsheet_dict = read_cheatsheet_data()
    section_dict.update(cheatsheet_dict)
    # Save updated dict
    write_cheatsheet_data(section_dict)
    # Update cheatsheet page
    refresh_cheatsheet_page()
    return 

def remove_cheatsheet_section(section):
    """ ->>
    Remove section (empty) from the cheatsheet_dict, 
    update the json file and refresh the .md page

    :param section: name of the new section
    :type section: str
    """
    cheatsheet_dict = read_cheatsheet_data()
    try: del cheatsheet_dict[section]
    except: pass
    # Save updated dict
    write_cheatsheet_data(cheatsheet_dict)
    # Update cheatsheet page
    refresh_cheatsheet_page()
    return 

def rename_cheatsheet_section(section, new_name):
    """ ->>
    Remove section (empty) from the cheatsheet_dict, 
    update the json file and refresh the .md page

    :param section: name of the new section
    :type section: str
    :param new_name: new name for the new section
    :type new_name: str
    """
    cheatsheet_dict = read_cheatsheet_data()
    new_cheatsheet_dict = OrderedDict((new_name if k == section else k, v) for k, v in cheatsheet_dict.items())
    # Save updated dict
    write_cheatsheet_data(new_cheatsheet_dict)
    # Update cheatsheet page
    refresh_cheatsheet_page()
    return 

def add_cheatsheet_command(section, cmd, description):
    """ ->>
    Add new record to the existing section of the cheatsheet_dict, 
    update the json file and refresh the .md page

    :param section: name of the new section
    :type section: str
    :param cmd: command
    :type cmd: str
    :param description: command description
    :type description: str
    """
    cheatsheet_dict = read_cheatsheet_data()
    # If section is not present, add it
    if section not in cheatsheet_dict:
        section_dict = OrderedDict([(section, {})])
        section_dict.update(cheatsheet_dict)
        cheatsheet_dict = section_dict
    # Generate unique code and add to section
    code = get_code()
    cheatsheet_dict[section][code] = {"cmd": cmd, "description": description}
    # Save updated dict
    write_cheatsheet_data(cheatsheet_dict)
    # Update cheatsheet page
    refresh_cheatsheet_page()
    return 

def remove_cheatsheet_command(section, code):
    """ ->>
    Remove record from the existing section of the cheatsheet_dict, 
    update the json file and refresh the .md page

    :param section: name of the new section
    :type section: str
    :param code: code identifier
    :type code: str
    """
    cheatsheet_dict = read_cheatsheet_data()
    del cheatsheet_dict[section][code] 
    # Save updated dict
    write_cheatsheet_data(cheatsheet_dict)
    # Update cheatsheet page
    refresh_cheatsheet_page()
    return 

def update_cheatsheet_command(section, code, cmd=None, description=None): 
    """ ->>
    Update record in the existing section of the cheatsheet_dict: code, description or both. 
    Update the json file and refresh the.md page 

    :param section: name of the new section
    :type section: str
    :param cmd: new command
    :type cmd: str
    :param description: new description
    :type description: str
    """
    if cmd is None and description is None: 
        return
    cheatsheet_dict = read_cheatsheet_data()
    if cmd is not None:
        cheatsheet_dict[section][code]["cmd"] = cmd 
    if description is not None:
        cheatsheet_dict[section][code]["description"] = description
    # Save updated dict
    write_cheatsheet_data(cheatsheet_dict)
    # Update cheatsheet page
    refresh_cheatsheet_page()
    return

def merge_cheatsheet_dicts(new_dict, cheatsheet_dict):
    """ ->>
    Merge new dict with the existing cheatsheet_dict. 
    First sections from new_dict will be taken. These sections 
    will be updated from the cheatsheet_dict too, if they are not 
    present in the respective section of the new_dict.   

    :param new_dict: new dict with sectios and commands
    :type cmd: OrderedDict
    :param cheatsheet_dict: existing cheatsheet_dict
    :type cheatsheet_dict: OrderedDict
    """
    # loop through the keys of the new dict, and update them from 
    #   the existing cheatsheet_dict
    for section, cmdlist in new_dict.items():
        # add commads from existing cheatsheet_dict, which are not 
        # present in the same section of the new_dict
        if section in cheatsheet_dict.keys():
            new_dict_section_commands = [i['cmd'] for k,i in new_dict[section].items()]
            for k,i in cheatsheet_dict[section].items():
                if i['cmd'] not in new_dict_section_commands:
                    new_dict[section][k] = i
    # now add sections from the existing cheatsheet_dict, which 
    #   are not present in the new_dict
    for section in cheatsheet_dict:
        if section not in new_dict:
            new_dict[section] = cheatsheet_dict[section]
    return new_dict
                          
def update_cheatsheet_page_from_new_dict(new_dict):
    """ ->>
    Update cheatsheet_dict with the new dict. The sections of the new dict 
    will be on top. If the same section name is already present in the 
    cheatsheet_dict, the new and old sections will be merged.

    :param new_dict: new dict with sectios and commands
    :type cmd: dict (or OrderedDict)
    """
    coded_dict = OrderedDict()
    # transform new_dict to have codes 
    for section, lists in new_dict.items():
        coded_dict[section] = {}
        for i in lists:
            code = get_code() 
            coded_dict[section][code] = i
    # read existing cheatsheet_dict and merge with the new
    cheatsheet_dict = read_cheatsheet_data()
    merged_dict = merge_cheatsheet_dicts(coded_dict, cheatsheet_dict)
    # Save updated dict
    write_cheatsheet_data(merged_dict)
    # Update cheatsheet page
    refresh_cheatsheet_page()
    return 