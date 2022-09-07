""" 
Methods to read/write workspace files, where meta, ui configs are defined
"""
import os
import logging
import time
import json, yaml
from jinja2 import Template
from .globals import *
from .ui_styles import styles_str

mkdocs_yml_path = os.path.join(WORKSPACE_UI_DIR, 'mkdocs.yml') 
ui_dict_file = os.path.join(WORKSPACE_UI_DIR, 'conf', 'ui-apps.json')
WORKSPACE_ABOUT_FILE = os.path.join(WORKSPACE_UI_DIR, 'docs', 'about.md')
WORKSPACE_MANIFEST_FILE = os.path.join(WORKSPACE_UI_DIR, 'docs', 'manifest.txt')
ZSHRC_FILE = os.path.join(HOME_DIR, '.zshrc')


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


def force_refresh_ui():
    """ Force UI to reload by updating manifest """
    with open(WORKSPACE_MANIFEST_FILE, 'w') as f:
        f.write(str(time.time()))
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
    # Force refresh UI
    force_refresh_ui()
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


def read_styles_scss():
    """ ->> {}
    Reads the UI styles of the runnning Workspace (.wrk), 
    parses and and returns the dict of styles. 
    """
    def get_color(line):
        parts = line.split(":")
        colpart = parts[1]
        for p in parts: 
            if "#" in p: colpart = p
        col_ = colpart.replace(";","")
        col_ = col_.replace("\n","")
        col_ = col_.replace("\t","")
        col_ = col_.replace("!important","")
        col_ = col_.strip()
        return col_

    def col_map(line, group, styles_dict):
        if "--md-primary-fg-color" in line:             styles_dict[group]["primary"] = get_color(line)
        elif "--md-accent-fg-color" in line:            styles_dict[group]["accent"] = get_color(line)
        elif "--md-default-bg-color" in line:           styles_dict[group]["background"] = get_color(line)
        elif "--md-default-fg-color--light" in line:    styles_dict[group]["subtitle"] = get_color(line)
        elif "--md-typeset-color" in line:              styles_dict[group]["text"] = get_color(line)
        elif "--md-typeset-a-color" in line:            styles_dict[group]["title"] = get_color(line)
        elif "--md-code-bg-color" in line:              styles_dict[group]["code_background"] = get_color(line)
        elif "--md-code-fg-color" in line:              styles_dict[group]["code_text"] = get_color(line)
        elif "--md-code-fg-color" in line:              styles_dict[group]["code_text"] = get_color(line)
        return styles_dict

    with open(WORKSPACE_UI_SCSS_STYLES_FILE) as styles_file:
        styles_lines = styles_file.readlines()
    styles_dict = {}
    group = ""
    for idx, line in enumerate(styles_lines):
        if 'data-md-color-scheme="workspace"' in line:
            group = "light"
            styles_dict[group] = {}
        elif 'data-md-color-scheme="workspace-dark"' in line:
            group = "dark"
            styles_dict[group] = {}
        elif ".md-header" in line:
            if "common_colors" not in styles_dict: styles_dict["common_colors"] = {}
            for nl in range(1,20):
                next_line = styles_lines[idx + nl]
                if "#" in next_line:
                    styles_dict["common_colors"]['header'] = get_color(next_line)
                    break
        elif ".md-nav__link--active" in line:
            if "common_colors" not in styles_dict: styles_dict["common_colors"] = {}
            for nl in range(1,20):
                next_line = styles_lines[idx + nl]
                if "#" in next_line:
                    styles_dict["common_colors"]['nav'] = get_color(next_line)
                    break
        else:
            styles_dict = col_map(line, group, styles_dict)
    return styles_dict


def write_styles_scss(styles_dict):
    """ {} ->> 
    Overwrite existing styles of the runnning Workspace (.wrk)

    :param styles_dict: dict with the updated styles
    :type meta_dict: dict
    """
    # Generate jinja template
    tm = Template(styles_str)
    new_styles_str = tm.render({'styles': styles_dict})
    with open(WORKSPACE_UI_SCSS_STYLES_FILE, "w") as styles_file:
        styles_file.write(new_styles_str)
    return


def read_zshrc():
    """ ->> [str]

    Read .zshrc file line-by-line
    :return: list with ~/.zshrc lines
    :rtype: list
    """
    with open(ZSHRC_FILE) as f:
        zshrc_lines = f.readlines()
    return zshrc_lines


def overwrite_zshrc(new_lines):
    """ [{},{}] ->>
   
    Overwrite .zshrc file line-by-line
    :param new_lines: list with new lines for ~/.zshrc
    :type new_lines: list
    """
    with open(ZSHRC_FILE, "w") as f:
        f.writelines(new_lines)
    return
    

def add_zshrc_line(line):
    """ str ->> 

    Add line to the ~/.zshrc file
    :param line: new line to add to the  ~/.zshrc file 
    :type line: str
    """
    with open(ZSHRC_FILE, "a") as f:
        # Append 'hello' at the end of file
        f.write(line)
    return
