"""
Module with functions to manage metsa.json and 'Abuot' 
tab in the workspace UI
"""
import os 
import logging
import json, yaml
import click
import configparser
from pathlib import Path
from distutils.dir_util import copy_tree
from datetime import date
from .conf_parser import read_conf_dir
from jinja2 import Template
from .globals import *
from .fileops import *
from .templates import *

WORKSPACE_ABOUT_FILE = os.path.join(WORKSPACE_UI_DIR, 'docs', 'about.md')

def get_ports_table():
    """  ->> str
    Returns info (as Markdown table) about all the ports 
    (within the range 8020-8040) that are used by the Workspace.

    :return: Markdown table with ports and applications in the workspace
    :rtype: str
    """
    ui_conf = read_ui_conf()
    ports = []
    for page, apps in ui_conf.items():
        for k,v in apps.items():
            ports.append({"port":v["port"], "title": v["title"], "page": page})
    # sort ports
    ports = sorted(ports, key=lambda l: l["port"])
    # Generate markdown template
    tm = Template(port_usage_template)
    port_info = tm.render(data={"ports":ports})
    return port_info


def get_startup_apps_table():
    """  ->> str

    Returns info (as Markdown table) about all the applications 
    started in the Workspace (when run/start the image) using supervisord.

    :return: Markdown table with startup applications of the workspace
    :rtype: str
    """
    startup_apps = []
    # read startup apps from the supervisord folder
    for f in os.listdir(SUPERVISORD_FOLDER):
        if ".conf" in f and f not in ['supervisord.conf', 'unified-supervisord.conf', 'mkdocs.conf']:
            config = configparser.ConfigParser()
            config.read(os.path.join(SUPERVISORD_FOLDER, f))
            for sec in config.sections():
                app = sec.split(":")[1]
                s = config[sec]
                cmd = s['command']
                startup_apps.append({"app": app, "cmd": cmd})
    # generate Markdown table string from the template
    tm = Template(startup_apps_template)
    startup_apps_str = tm.render(data={"startup_apps":startup_apps})
    return startup_apps_str


def get_lineage_table():
    """  ->> str

    Returns lineage table (as Markdown table). This workspace is excluded from the 
    lineage table. 

    :return: Markdown table with history of this workspace lineage
    :rtype: str
    """
    lineage = read_lineage()
    max_ind = max([e["ind"] for e in lineage])
    # remove current workspace from the lineage
    lineage = [l for l in lineage if l["ind"] != max_ind] 
    # order lineage in desc order
    lineage = sorted(lineage, key=lambda d: d['ind'], reverse=True) 
    # generate Markdown table string from the template
    tm = Template(lineage_template)
    lineage_str = tm.render(data={"lineage":lineage})
    return lineage_str


def add_wrk_to_lineage(name, version, docs):
    """ str, str, str ->> 
    Add this workspace to the workspace lineage file.

    :param wrk_name: workspace name
    :type wrk_name: str
    :param version: workspace version
    :type version: str
    :param docs_link: link to the workspace documentation
    :type docs_link: str
    """
    # read lineage file
    lineage = read_lineage()
    # get last index
    max_ind = max([e["ind"] for e in lineage])
    new_ind = max_ind + 1
    # add element to the dict
    lineage.append(
        {"ind": new_ind, "name": name, "version": version, "link": docs}
    )
    # save updated lineage
    write_lineage(lineage)
    return


def update_meta(name=None, version=None, author=None, description=None, update_created=True):
    """ str, str, str, str, bool ->> 
    Updates meta.json. When called without any args, it will 
    update 'created' field only. 

    :param name: workspace name
    :type name: str
    :param version: workspace version
    :type version: str
    :param author: workspace author
    :type author: str
    :param description: workspace description
    :type description: str
    :param update_created: should 'created' be updated in the meta.json? (Default is True)
    :type update_created: bool
    """
    meta_dict = read_meta()
    if name is not None:
        meta_dict['name'] = name
    if version is not None:
        meta_dict['version'] = version
    if author is not None:
        meta_dict['author'] = author
    if description is not None:
        meta_dict['description'] = description
    if update_created:
        meta_dict['created'] = str(date.today())
    write_meta(meta_dict)
    return


def refresh_about():
    """  ->>
    Read meta.json, use its values for the about_page_template,
    and overwrite the about.md page
    """
    # First get all the meta info
    meta_dict = read_meta()
    # Add ports table
    meta_dict['ports_table'] = get_ports_table()
    # Add scheduled apps table
    meta_dict['startup_table'] = get_startup_apps_table()
    # Add lineage table
    meta_dict['lineage_table'] = get_lineage_table()
    # Generate template for the About page
    tm = Template(about_page_template)
    new_about = tm.render(meta_dict)
    write_about(new_about)


def update_workspace_name(new_name):
    """ str ->>
    Update name of this workspace
    """
    # update meta with the new workspace name
    update_meta(name=new_name)
    # update about page with the new name
    refresh_about() 
    return


def update_workspace_version(new_version):
    """ str/int/float ->>
    Update name of this workspace
    """
    # update meta with the new workspace version
    update_meta(version=new_version)
    # update about page with the new version
    refresh_about() 
    return


def update_workspace_author(new_author):
    """ str ->>
    Update author of this workspace
    """
    # update meta with the new author
    update_meta(author=new_author)
    # update about page with the new author
    refresh_about() 
    return


def update_workspace_description(new_description):
    """ str ->>
    Update author of this workspace
    """
    # update meta with the new description
    update_meta(description=new_description)
    # update about page with the new description
    refresh_about() 
    return


def edit_workspace_description():
    """  ->>
    Interactively edit the description of the aboput page. 
    It calls system editor for that.
    """
    # Get description from meta
    wrk_meta = read_meta()
    # input new description interactively, using external text editor
    new_description = click.edit(editor=TEXT_EDITOR, text=wrk_meta['description'])
    # update meta of this workspace
    update_meta(description=new_description)
    # update about page with the new description
    refresh_about() 
    return