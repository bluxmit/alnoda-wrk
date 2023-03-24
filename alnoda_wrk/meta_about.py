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
from datetime import date, datetime
from .conf_parser import read_conf_dir
from jinja2 import Template
from .globals import *
from .fileops import *
from .templates import *

WORKSPACE_ABOUT_FILE = os.path.join(WORKSPACE_UI_DIR, 'docs', 'about.md')
ALNODA_APPS_KEY = 'alnoda.org.apps'

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
    ports = sorted(ports, key=lambda l: int(l["port"]))
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


def better_tags(tags):
    """ str ->> str

    Beautify tags for Markdown - wrap in backtics, split by space
    :param tags: comma-separated tags
    :type name: str
    :return: beautified tags
    :rtype: str
    """
    tags_list = tags.split(",")
    b_tags = " ".join([f"`{tag}`" for tag in tags_list if tag != ""])
    return b_tags


def get_lineage_table():
    """  ->> str

    Returns lineage table (as Markdown table). This workspace is excluded from the 
    lineage table. 

    :return: Markdown table with history of this workspace lineage
    :rtype: str
    """
    lineage = read_lineage()
    max_ind = max([e["ind"] for e in lineage])
    # # remove current workspace from the lineage
    # lineage = [l for l in lineage if l["ind"] != max_ind] 
    # beautify tags in lineage 
    for l in lineage:
        if 'tags' in l: l['tags'] = better_tags(l['tags'])
    # order lineage in desc order
    lineage = sorted(lineage, key=lambda d: d['ind'], reverse=True) 
    # generate Markdown table string from the template
    tm = Template(lineage_template)
    lineage_str = tm.render(data={"lineage":lineage})
    return lineage_str


def add_wrk_to_lineage(name, version, docs, tags):
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
        {"ind": new_ind, "name": name, "version": version, "link": docs, "tags": tags}
    )
    # save updated lineage
    write_lineage(lineage)
    return


def update_meta(name=None, version=None, author=None, description=None, docs=None, tags=None, repository=None):
    """ str, str, str, str, bool ->> 
    Updates meta.json. When called without any args, it will ensure 
    that 'workspace_id' and 'created' fields are added to meta. 

    :param name: workspace name
    :type name: str
    :param version: workspace version
    :type version: str
    :param author: workspace author
    :type author: str
    :param description: workspace description
    :type description: str
    :param docs: link to the workspace documentation
    :type docs: str
    :param repository: link to the workspace source code
    :type repository: str
    :param update_created: should 'created' be updated in the meta.json? (Default is True)
    :type update_created: bool
    """
    meta_dict = read_meta()
    # if workspace_id not yet in meta - generate new, and add it to meta
    if 'workspace_id' not in meta_dict: meta_dict['workspace_id'] = get_code(length=16)
    if 'created' not in meta_dict: meta_dict['created'] = datetime.today().strftime('%Y-%m-%d')
    # update meta_dict with the respective input
    if name is not None:
        meta_dict['name'] = name
    if version is not None:
        meta_dict['version'] = version
    if author is not None:
        meta_dict['author'] = author
    if description is not None:
        meta_dict['description'] = description
    if docs is not None:
        meta_dict['docs'] = docs
    if repository is not None:
        meta_dict['repository'] = repository
    if tags is not None:    meta_dict['tags'] = tags.lower()
    else:   meta_dict['tags'] = ""
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
    # Beautify tags
    if 'tags' in meta_dict and meta_dict['tags'] != "":
        meta_dict['tags'] = better_tags(meta_dict['tags'])
    # Add lineage table
    meta_dict['lineage_table'] = get_lineage_table()
    meta_dict['lineage_table'] = get_lineage_table()
    # Generate template for the About page
    tm = Template(about_page_template)
    new_about = tm.render(meta_dict)
    write_about(new_about)
    return


def refresh_from_meta():
    """ ->>
    Refreshes from meta both about page, and mkdocs.yaml (in the .wrk)
    """
    refresh_about()
    # Refresh workspace name on the main page too
    meta_dict = read_meta()
    mkdocs_dict = get_mkdocs_yml()
    mkdocs_dict['site_name'] = meta_dict['name']
    # Refresh workspace docs link on the main page too
    doc_url = meta_dict['docs']
    if 'http' not in doc_url or 'https' not in doc_url: doc_url = "https://"+doc_url
    for e in mkdocs_dict['nav']:
        if 'Docs' in e: e['Docs'] = doc_url
    # write updated mkdocs dict
    update_mkdocs_yml(mkdocs_dict)
    return


def update_workspace_name(new_name):
    """ str ->>
    Update name of this workspace
    """
    # update meta with the new workspace name
    update_meta(name=new_name)
    # update about page with the new name
    refresh_about() 
    # update mkdocs.yaml with the new name
    mkdocs_dict = get_mkdocs_yml()
    mkdocs_dict['site_name'] = new_name
    update_mkdocs_yml(mkdocs_dict)
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
    Update description of this workspace
    """
    # update meta with the new description
    update_meta(description=new_description)
    # update about page with the new description
    refresh_about() 
    return


def update_workspace_tags(new_tags):
    """ str ->>
    Update tags of this workspace
    """
    # update meta with the new tags
    update_meta(tags=new_tags)
    # update about page with the new tags
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


def get_workspace_id():
    """  ->> str
    Simply return workspace id from meta

    :return: Markdown table with history of this workspace lineage
    :rtype: str
    """
    meta_dict = read_meta()
    return meta_dict['workspace_id']


def app_already_installed(app_code):
    """  ->> str
    Check if app is already installed and present in the meta

    :param app_code: app code on the alnoda.org
    :type app_code: str
    :return: is app code present in meta?
    :rtype: bool
    """
    meta_dict = read_meta()
    if ALNODA_APPS_KEY not in meta_dict: return False
    else:
        if app_code in meta_dict[ALNODA_APPS_KEY]:
            return True
    return False


def is_port_in_app_use(port):
    """ Check if alnoda apps do not use this port """
    meta_dict = read_meta()
    if "alnoda.org.apps" not in meta_dict: return False
    for k,v in meta_dict['alnoda.org.apps']:
        if "port" in v and v['port'] == port: return True
    return False


def log_app_installed(app_code, name, version, desctiption, app_port=None):
    """  ->> str
    Log in meta that some app is installed

    :param app_code: app code on the alnoda.org
    :type app_code: str
    :param name:  app name on the alnoda.org
    :type name: str
    :param version:  app version on the alnoda.org
    :type version: str
    :param desctiption:  app description on the alnoda.org
    :type desctiption: str
    : param app_port: port app is listening to
    :type app_port: int
    """
    meta_dict = read_meta()
    # if apps is not yet present in meta - add it
    if ALNODA_APPS_KEY not in meta_dict:
        meta_dict[ALNODA_APPS_KEY] = {}
    # if this app is already present - return
    if app_code in meta_dict[ALNODA_APPS_KEY]: return
    # add app to meta and save meta
    meta_dict[ALNODA_APPS_KEY][app_code] = {
        'name': name,
        'version': version,
        'desctiption': desctiption,
        'date': datetime.today().strftime('%Y-%m-%d'),
        'app_port': app_port
    }
    write_meta(meta_dict)
    return


