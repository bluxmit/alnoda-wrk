import os 
import logging
import json, yaml
from jinja2 import Template
from collections import OrderedDict
from .globals import *
from .templates import links_template

LINKS_DATA_FILE = os.path.join(WORKSPACE_DIR, 'links.json') 
WORKSPACE_LINKS_FILE = os.path.join(WORKSPACE_UI_DIR, 'docs', 'links.md')

def read_links_data():
    """ ->> {}
    Reads existing links data json file, and returns dict.

    :return: existing links as dict
    :rtype: OrderedDict
    """
    if not os.path.exists(LINKS_DATA_FILE):
        with open(LINKS_DATA_FILE, "x") as f:
            f.write("{}")
    with open(LINKS_DATA_FILE) as json_file:
        links_dict = json.load(json_file)
    return OrderedDict(links_dict)

def write_links_data(links_dict):
    """ {} ->> 
    Overwrite existing links json with the updated dict

    :param links_dict: dict with the updated links
    :type links_dict: OrderedDict
    """
    with open(LINKS_DATA_FILE, 'w') as file:
        json.dump(links_dict, file, indent=4 * ' ')
    return 

def refresh_links_page():
    """ ->>
    Refreshes from links dict the respective worksapce page (in the .wrk)
    """
    # read links json
    links_dict = read_links_data()
    # generate page from template
    tm = Template(links_template)
    links_page = tm.render(data=links_dict)
    # overwrite links.md page
    with open(WORKSPACE_LINKS_FILE, "w") as links_md_file:
        links_md_file.write(links_page)
    return 
    
def add_links_section(section):
    """ ->>
    Add new section (empty) to the links dict, 
    update the json file and refresh the .md page

    :param section: name of the new section
    :type section: str
    """
    # Add section in the beginning
    section_dict = OrderedDict([(section, {})])
    links_dict = read_links_data()
    section_dict.update(links_dict)
    # Save updated dict
    write_links_data(section_dict)
    # Update links .md page
    refresh_links_page()
    return 

def remove_links_section(section):
    """ ->>
    Remove section (empty) from the links dict, 
    update the json file and refresh the .md page

    :param section: name of the new section
    :type section: str
    """
    links_dict = read_links_data()
    try: del links_dict[section]
    except: pass
    # Save updated dict
    write_links_data(links_dict)
    # Update cheatsheet page
    refresh_links_page()
    return 

def rename_links_section(section, new_name):
    """ ->>
    Remove section (empty) from the links dict, 
    update the json file and refresh the .md page

    :param section: name of the new section
    :type section: str
    :param new_name: new name for the new section
    :type new_name: str
    """
    links_dict = read_links_data()
    new_links_dict = OrderedDict((new_name if k == section else k, v) for k, v in links_dict.items())
    # Save updated dict
    write_links_data(new_links_dict)
    # Update links page
    refresh_links_page()
    return 

def add_links_url(section, url, name, description):
    """ ->>
    Add new record to the existing section of the links dict, 
    update the json file and refresh the .md page

    :param section: name of the new section
    :type section: str
    :param url: new url
    :type url: str
    :param name: new link name
    :type name: str
    :param description: command description
    :type description: str
    """
    links_dict = read_links_data()
    # If section is not present, add it
    if section not in links_dict:
        section_dict = OrderedDict([(section, {})])
        section_dict.update(links_dict)
        links_dict = section_dict
    # Generate unique code and add to section
    code = get_code()
    links_dict[section][code] = {"url": url, "name": name, "description": description}
    # Save updated dict
    write_links_data(links_dict)
    # Update links page
    refresh_links_page()
    return 

def remove_links_url(section, code):
    """ ->>
    Remove record from the existing section of the links dict, 
    update the json file and refresh the .md page

    :param section: name of the new section
    :type section: str
    :param code: code identifier
    :type code: str
    """
    links_dict = read_links_data()
    del links_dict[section][code] 
    # Save updated dict
    write_links_data(links_dict)
    # Update links page
    refresh_links_page()
    return 

def update_links_url(section, code, url=None, name=None, description=None): 
    """ ->>
    Update record in the existing section of the links dict: url, name, description or all. 
    Update the json file and refresh the.md page 

    :param section: section where to make changes
    :type section: str
    :param code: code of the url where to make changes
    :type code: str
    :param url: new url
    :type url: str
    :param name: new name
    :type name: str
    :param description: new description
    :type description: str
    """
    if url is None and name is None and description is None: 
        return
    links_dict = read_links_data()
    if url is not None:
        links_dict[section][code]["url"] = url 
    if name is not None:
        links_dict[section][code]["name"] = name 
    if description is not None:
        links_dict[section][code]["description"] = description
    # Save updated dict
    write_links_data(links_dict)
    # Update links page
    refresh_links_page()
    return

def merge_links_dicts(new_dict, links_dict):
    """ ->>
    Merge new dict with the existing links dict. 
    First sections from new_dict will be taken. These sections 
    will be updated from the links_dict too, if they are not 
    present in the respective section of the new_dict.   

    :param new_dict: new dict with sectios and commands
    :type cmd: OrderedDict
    :param links_dict: existing links dict
    :type links_dict: OrderedDict
    """
    # loop through the keys of the new dict, and update them from 
    #   the existing links_dict
    for section, url_list in new_dict.items():
        # add commads from existing links dict, which are not 
        # present in the same section of the new_dict
        if section in links_dict.keys():
            new_dict_section_urls = [i['url'] for k,i in new_dict[section].items()]
            for k,i in links_dict[section].items():
                if i['url'] not in new_dict_section_urls:
                    new_dict[section][k] = i
    # now add sections from the existing links dict, which 
    #   are not present in the new_dict
    for section in links_dict:
        if section not in new_dict:
            new_dict[section] = links_dict[section]
    return new_dict
                          
def update_links_page_from_new_dict(new_dict):
    """ ->>
    Update links page with the new dict. The sections of the new dict 
    will be on top. If the same section name is already present in the 
    linnks dict, the new and old sections will be merged.

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
    # read existing links dict and merge with the new
    links_dict = read_links_data()
    merged_dict = merge_links_dicts(coded_dict, links_dict)
    # Save updated dict
    write_links_data(merged_dict)
    # Update cheatsheet page
    refresh_links_page()
    return 