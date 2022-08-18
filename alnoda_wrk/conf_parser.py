"""
Simply parse configuration yaml file and validate inuts
"""
import logging
import os
from pathlib import Path
import yaml
import re
from cerberus import Validator
schema = eval(open(Path(__file__).with_name('config_schema.py'), 'r').read())

REQUIRED_KEYS = {
    'name': 'Workspace requires name. Please add to the workspace.yaml a key "name"',
    'doc_url': 'Workspace must have documentation. Please add to the workspace.yaml a key "doc_url" with the link to the documentation URL',
    'description': 'Workspace needs a description. Please add to the workspace.yaml a key "description" with a short description', 
    }
ALLOWED_IMAGE_EXTENSIONS = ["svg", "png", "jpeg", "jpg"]


def validate_main_required_keys_present(wrk_params):
    """ {} -> bool
    Validate presence of the required keys, raise exception of not found

    :param wrk_params: dict of workspace parameters
    :type wrk_params: dict
    :return: all main required keys are present
    :rtype: bool
    """
    for k, m in REQUIRED_KEYS.items():
        if k not in wrk_params.keys():
            raise Exception(m)
        elif wrk_params[k] is None or  wrk_params[k] == "":
            raise Exception(m)
        else:
            try:
                if wrk_params[k].isspace(): raise Exception(m)
            except: pass
    logging.debug('Main required keys are OK')
    return True


def validate_schema(wrk_params):
    """ {} -> bool
    Validate the config dict against the schema

    :param wrk_params: dict of workspace parameters
    :type wrk_params: dict
    :return: schema validation successful
    :rtype: bool
    """
    v = Validator(schema)
    valid = v.validate(wrk_params)
    if not valid:
        raise Exception(v.errors)
    logging.debug('workspace.yaml satisfies schema requirements')
    return True


def parse_config_file(conf_file):
    """ str -> {}
    Read workspace config file (workspace.yaml), validate and return config dict

    :param conf_file: config yaml file path
    :type conf_file: str
    :return: workspace parameters, parsed from the config file
    :rtype: dict
    :raises: exception if validator fails
    """
    with open(conf_file, 'r') as stream:
        wrk_params = yaml.safe_load(stream)
    # Validate main required fields are present
    validate_main_required_keys_present(wrk_params)
    # Validate workspace.yaml against the schema
    validate_schema(wrk_params)
    return wrk_params


def get_workspace_yaml(files):
    """ [] -> PosixPath 
    Get list of files in the workspace config, and validate workspace.yaml is present, 
    and it is a proper yaml file

    :param files: path to the config directory
    :type files: str
    :return: workspace parameters, parsed from the config file
    :rtype: dict
    """
    conf_file = None
    # Find if workspace config file is present 
    for f in files:
        if 'workspace.yaml' in str(f) or 'workspace.yml' in str(f):
            conf_file = f
            logging.debug(f'found workspace config file {conf_file}')
    if conf_file is None:
        raise Exception("workspace.yaml is missing in the workspace config folder")
    return conf_file


def valid_image_extension(img_name):
    """ str -> bool
    Validate image is among the supported ones

    :param img_name: image file name
    :type img_name: str
    :return: is image extension supported?
    :rtype: bool
    """
    for ext in ALLOWED_IMAGE_EXTENSIONS:
        if f".{ext}" in img_name:
            return True
    return False


def get_ui_images(wrk_params):
    """ {} -> []
    Recieves workspace parameters dict, and returns the list 
    of images that are used for the workspace Quickstart page.

    :param wrk_params: dict with parsed workspace parameters
    :type wrk_params: dict
    :return: list of images for the Quickstart page
    :rtype: list
    """
    required_images = []
    # First check if logo and favicon should have images
    if 'logo' in wrk_params:
        image_name = wrk_params["logo"]
        assert valid_image_extension(image_name), "Unsupported image type for logo"
        required_images.append(image_name)
    if 'favicon' in wrk_params:
        image_name = wrk_params["favicon"]
        assert valid_image_extension(image_name), "Unsupported image type for favicon"
        required_images.append(image_name)
    # Collect all images required for the Quickstart pages
    if "pages" in wrk_params:
        for page in wrk_params["pages"]:
            tool_list = wrk_params["pages"][page]  # <- list of dicts
            for tool in tool_list:
                image_name = tool['image']
                assert valid_image_extension(image_name), "Unsupported image type for Quickstart page"
                required_images.append(image_name)
    logging.debug(f"Workspace Quickstart UI requires the following images {required_images}")
    return required_images


def check_images_present(wrk_params, files=[]):
    """ {}, [] -> bool
    Recieves the list of files in the config folder,
    and the wrk_params dict. Identifies which images are used, 
    and check they are present in the config folder 

    :param wrk_params: dict with parsed workspace parameters
    :type wrk_params: dict
    :param files: list of PosixPath files from the config folder
    :rtype: list
    :return: all files mentioned in the workspace.yaml are present in the config folder
    :rtype: bool
    """
    def img_present(sub, slist):
        for s in slist:
            if sub in s: 
                logging.debug(f"found image {image_name} in {s}")
                return True
        return False
    required_images = get_ui_images(wrk_params)
    for image_name in required_images:
        logging.debug(f"looking for image {image_name}")
        if not img_present(image_name, [str(f) for f in files]):
            raise Exception(f"Image {image_name} is defined in the workspace.yaml file, but it is not present in the same folder")
    return True

    
def read_conf_dir(conf_dir_path):
    """ str -> {}, [] 
    Read workspace config folder, get list of files
    Read and validate workspace.yaml
    Check all required files (i.e. images) are present

    :param conf_dir_path: path to the config directory
    :type conf_dir_path: str
    :return: workspace parameters, parsed from the config file
    :rtype: dict
    :return: files in the config folder
    :rtype: list
    """
    # First of all, check such folder even exists
    if not Path(conf_dir_path).is_dir():
        raise Exception(f"Folder {conf_dir_path} does not exist!")
    # Search Directories Recursively
    #files = list(filter(lambda x: x.is_file(), Path(conf_dir_path).rglob('*')))  # incl. subdirs
    files = list(filter(lambda x: x.is_file(), Path(conf_dir_path).iterdir()))    # only one dir
    for f in files: logging.debug(f"found file {f}")
    # Get workspace config yaml file
    conf_file = get_workspace_yaml(files)
    # Parse and validate config file, get workspace params
    wrk_params = parse_config_file(str(conf_file))
    # Check all images are present
    check_images_present(wrk_params, files)
    return wrk_params, files

