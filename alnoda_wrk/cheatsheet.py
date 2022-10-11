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
    # Try to add to the section, if exists
    try: cheatsheet_dict[section][cmd] = description
    except: pass
    # Save updated dict
    write_cheatsheet_data(cheatsheet_dict)
    # Update cheatsheet page
    refresh_cheatsheet_page()
    return 

def remove_cheatsheet_command(section, cmd):
    """ ->>
    Remove record from the existing section of the cheatsheet_dict, 
    update the json file and refresh the .md page

    :param section: name of the new section
    :type section: str
    :param cmd: command
    :type cmd: str
    """
    cheatsheet_dict = read_cheatsheet_data()
    try: del cheatsheet_dict[section][cmd]
    except: pass
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
    for section, cmds in new_odict.items():
        # if this key is present in the existing cheatsheet_dict - 
        #   add keys cheatsheet_dict to the new_odict
        if section in cheatsheet_dict.keys():
            for cmd, descr in cheatsheet_dict[section].items():
                if cmd not in new_odict[section]:
                    new_odict[section][cmd] = descr
    # Now add sections from the existing cheatsheet_dict, which 
    #   are not present in the new_odict
    for section in cheatsheet_dict:
        if section not in new_odict:
            new_dict[section] = cheatsheet_dict[section]
    return new_dict
                          
def update_cheatsheet_page_from_new_dict(new_dict):
    """ ->>
    Update cheatsheet_dict with the new dict. The sections of the new dict 
    will be on top. If the same section name is already present in the 
    cheatsheet_dict, the new and old sections will be merged.

    :param section: name of the new section
    :type section: str
    :param new_dict: new dict with sectios and commands
    :type cmd: dict (or OrderedDict)
    """
    new_odict = OrderedDict(new_dict)
    cheatsheet_dict = read_cheatsheet_data()
    merged_dict = merge_cheatsheet_dicts(new_odict, cheatsheet_dict)
    # Save updated dict
    write_cheatsheet_data(merged_dict)
    # Update cheatsheet page
    refresh_cheatsheet_page()
    return 
