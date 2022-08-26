""" 
Methods to read/write workspace files, where meta, ui configs are defined
"""
import os
import logging
import json, yaml
from .globals import *

mkdocs_yml_path = os.path.join(WORKSPACE_UI_DIR, 'mkdocs.yml') 
ui_dict_file = os.path.join(WORKSPACE_UI_DIR, 'conf', 'ui-apps.json')
WORKSPACE_ABOUT_FILE = os.path.join(WORKSPACE_UI_DIR, 'docs', 'about.md')

def get_mkdocs_yml():
    """  ->> {}
    Reads mkdocs.yml from the workspace UI, and returns as dict

    :return: workspace mkdocs.yml as a dict
    :rtype: dict
    """
    logging.debug(f"reading mkdocs.yml from {mkdocs_yml_path}")
    with open(mkdocs_yml_path, 'r') as stream:
        mkdocs_dict = yaml.safe_load(stream)
    return mkdocs_dict


def update_mkdocs_yml(mkdocs_dict):
    """ {} ->> 
    Updates (replaces) mkdocs.yml with the new dict

    :param mkdocs_dict: dict with main configuration for MkDocs
    :type wrk_params: dict
    """
    with open(mkdocs_yml_path, 'w') as file:
        documents = yaml.dump(mkdocs_dict, file, default_flow_style=False)
    return


def read_ui_conf():
    """ ->> {}
    Reads existing workspace UI json, and returns dict.

    :return: existing UI app configuration
    :rtype: dict
    """
    with open(ui_dict_file) as json_file:
        ui_apps = json.load(json_file)
    return ui_apps


def update_ui_conf(ui_apps):
    """ {} ->> 
    Overwrite existing workspace UI json with the updated dict

    :param ui_apps: dict with the current MkDocs pages, fetched from the .wrk dir
    :type ui_apps: dict
    """
    with open(ui_dict_file, 'w') as file:
        json.dump(ui_apps, file, indent=4 * ' ')
    return 


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


def read_lineage():
    """ ->> {}
    Reads existing lineage dict file.

    :return: dict with workspace lineage
    :rtype: dict
    """
    with open(WORKSPACE_LINEAGE_FILE) as json_file:
        wrk_meta = json.load(json_file)
    return wrk_meta


def write_lineage(meta_dict):
    """ {} ->> 
    Overwrite existing lineage json with the updated dict

    :param meta_dict: dict with the updated lineage
    :type meta_dict: dict
    """
    with open(WORKSPACE_LINEAGE_FILE, 'w') as file:
        json.dump(meta_dict, file, indent=4 * ' ')
    return 
