import os 
import logging
import json, yaml
from pathlib import Path
import shutil
from .meta_about import update_meta, refresh_about, add_wrk_to_lineage, refresh_from_meta
from .conf_parser import read_conf_dir
from .globals import *
from .ui_builder import build_wrk_ui
from .wrk_supervisor import init_supervisord, create_supervisord_file
from .cheatsheet import update_cheatsheet_page_from_new_dict
from .links import update_links_page_from_new_dict

MKDOCS_REQUIREMENTS_DIR = os.path.join(WORKSPACE_DIR, 'requires')
mkdocs_file = os.path.join(MKDOCS_REQUIREMENTS_DIR, 'mkdocs.txt')
mkdocs_deps_file = os.path.join(MKDOCS_REQUIREMENTS_DIR, 'deps.txt')


def install_mkdocs_deps():
    """ Install mkdocs dependencies with pipx """
    # Try to uninstall mkdocs (we want to update the version if any)
    try:
        uninstall_mkdocs = os.popen("pipx uninstall mkdocs").read()
        logging.debug(uninstall_mkdocs)
    except Exception as e:
        logging.debug(f"Error uninstalling mkdocs: {e}")
    # Read mkdocs and mkdocs-requirements
    with open(mkdocs_file) as f:
        mkdocs = f.read()
    with open(mkdocs_deps_file) as f:
        mkdocs_requirements = f.readlines()
    # Install new mkdocs & dependencies with pipx
    install_mkdocs_res = os.popen(f"pipx install {mkdocs}").read()
    logging.debug(install_mkdocs_res)
    for dependency in mkdocs_requirements:
        install_mkdocs_deps_res = os.popen(f"pipx inject mkdocs {dependency}").read()
        logging.debug(install_mkdocs_deps_res)
    return


def init_wrk():
    """  ->> bool
    Check if this workspace has UI folder. If not copy the 
    boilerplate - the default starting UI

    :return: whether workspace was successfully initialized
    :rtype: bool
    """
    logging.debug(f'checking workspace initialized in folder {WORKSPACE_DIR}')
    try:
        if not Path(WORKSPACE_DIR).is_dir():
            this_path = os.path.dirname(os.path.realpath(__file__))
            shutil.copytree(os.path.join(this_path, 'wrk'), WORKSPACE_DIR)
            # update meta 
            update_meta()   #<- generate workspace ID and save created date
            refresh_about() #<- and update about page with the new date
        else:
            logging.info(f'Workspace initialized in {WORKSPACE_DIR}')
    except Exception as e:
        logging.warning(f"Something went wrong. Is workspace folder deleted? Error: {e}")
        return False
    install_mkdocs_deps() #<- install all dependencies for mkdocs
    return True


def delete_wrk():
    """ Delete workspace folder: UI and metadata """
    if Path(WORKSPACE_DIR).is_dir():
        shutil.rmtree(WORKSPACE_DIR)
        logging.warning("Workspace UI deleted!")
    return


def create_startup_applications(wrk_params):
    """ {} ->> 
    Read wrk_params, identify applications, and create startup 
    supervisord files.

    :param wrk_params: dict with the workspace parameters
    :type wrk_params: dict
    """
    if 'start' in wrk_params:
        for startup_app in wrk_params['start']:
            # make sure app name is 'safe' for supervisord name
            startup_app['name'] = safestring(startup_app['name'])
            # transform env_vars (if provided into list) from list of dicts into list of strings
            if 'env_vars' in startup_app:
                tr_env_vars = []
                for ev in startup_app['env_vars']:
                    tr_env_vars.append(ev["name"]+"="+ev["value"])
                startup_app['env_vars'] = tr_env_vars
            create_supervisord_file(**startup_app)
    return
        

def build_workspace(conf_dir_path):
    """ str ->>
    Builds/updates UI based on the cofigs folder provided by the user. 
    Config folder must have file ui_config.yaml, and all images that are used to the UI.

    :param conf_dir_path: path to the config directory
    :type conf_dir_path: str
    """
    initialized = init_wrk()  # <- First make sure UI is initiated
    if not initialized:
        raise Exception("There was a problem initializing workspace UI")
    # Read new user configs_dir
    wrk_params, files = read_conf_dir(conf_dir_path)
    # Update meta.json and refresh About page 
    update_meta(
        name = wrk_params['name'],
        version = wrk_params['version'],
        author = wrk_params['author'],
        description = wrk_params['description']
    )
    # Create UI
    build_wrk_ui(wrk_params, conf_dir_path)
    # Create supervisord files for applications to start up
    create_startup_applications(wrk_params)
    # Add this workspace to the lineage
    tags = ""
    if 'tags' in wrk_params:
        tags = wrk_params['tags']
    add_wrk_to_lineage(
        name = wrk_params['name'],
        version = wrk_params['version'],
        docs = wrk_params['doc_url'],
        tags = tags
        )
    # Refresh about page
    refresh_from_meta()
    # Update cheatsheet page 
    if 'cheatsheet' in wrk_params:
        update_cheatsheet_page_from_new_dict(wrk_params['cheatsheet'])
    else:
        update_cheatsheet_page_from_new_dict({})
    # Update links page 
    if 'links' in wrk_params:
        update_links_page_from_new_dict(wrk_params['links'])
    else:
        update_links_page_from_new_dict({})
    return
    