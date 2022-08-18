"""
Module with functions to manage metsa.json and 'Abuot' 
tab in the workspace UI
"""
import os 
import logging
import json, yaml
import click
from pathlib import Path
from distutils.dir_util import copy_tree
from datetime import date
from .conf_parser import read_conf_dir
from jinja2 import Template
from .globals import *
from .templates import about_page_template

WORKSPACE_ABOUT_FILE = os.path.join(WORKSPACE_UI_DIR, 'docs', 'about.md')


def read_meta():
    """ ->> {}
    Reads existing workspace UI json, and returns dict.

    :return: dict with workspace meta data
    :rtype: dict
    """
    with open(WORKSPACE_META_FILE) as json_file:
        wrk_meta = json.load(json_file)
    return wrk_meta


def write_meta(meta_dict):
    """ {} ->> 
    Overwrite existing workspace meta data json with the updated dict

    :param meta_dict: dict with the updated meta
    :type meta_dict: dict
    """
    with open(WORKSPACE_META_FILE, 'w') as file:
        json.dump(meta_dict, file, indent=4 * ' ')
    return 


def read_about():
    """ ->> str, str
    Reads MkDocs about.md file, strips out the header template
    and returns only the text from the About section

    :return: header section of the About page
    :rtype: str
    :return: description section of the About page
    :rtype: str
    """
    with open(WORKSPACE_ABOUT_FILE) as f:
        about = f.read()
    return about


def write_about(about):
    """ str ->> 
    Only updates the "Description" section, leaving header the same

    :param about: new content for the 'About' page
    :type about: str
    """
    with open(WORKSPACE_ABOUT_FILE, 'w') as f:
        f.write(about)
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


def refresh_about_from_meta():
    """  ->>
    Read meta.json, use its values for the about_page_template,
    and overwrite the about.md page
    """
    meta_dict = read_meta()
    tm = Template(about_page_template)
    new_about = tm.render(meta_dict)
    write_about(new_about)


def update_workspace_name(new_name):
    """ str ->>
    Update name of this workspace
    """
    # update meta with the new workspace
    update_meta(name=new_name)
    # update about page with the new description
    refresh_about_from_meta() 
    return


def update_workspace_version(new_version):
    """ str/int/float ->>
    Update name of this workspace
    """
    # update meta with the new workspace
    update_meta(version=new_version)
    # update about page with the new description
    refresh_about_from_meta() 
    return


def update_workspace_author(new_author):
    """ str ->>
    Update author of this workspace
    """
    # update meta with the new author
    update_meta(author=new_author)
    # update about page with the new description
    refresh_about_from_meta() 
    return


def edit_workspace_description():
    """  ->>
    Interactively edit the description of the aboput page. 
    It calls nano editor for that.
    """
    # Get description from meta
    wrk_meta = read_meta()
    # input new description interactively, using external text editor
    new_description = click.edit(editor=TEXT_EDITOR, text=wrk_meta['description'])
    # update meta of this workspace
    update_meta(description=new_description)
    # update about page with the new description
    refresh_about_from_meta() 
    return