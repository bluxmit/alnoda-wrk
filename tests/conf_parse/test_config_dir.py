import pytest
from pathlib import Path, PosixPath
from alnoda_wrk.conf_parser import *
from tests.conf_parse.test_config_parser import read_test_conf
import yaml
import os


def get_full_conf_dir_path(conf_dir_path):
    dirpath = os.path.dirname(Path(__file__))
    fullpath = f"{dirpath}/workspace-dirs/{conf_dir_path}"
    return fullpath

def test_get_workspace_yaml():
    """ Test that workspace yaml file is found
    """
    files = [PosixPath('/home/works/IDE_copy.jpg'), PosixPath('/home/works/Htop.jpg'), PosixPath('/home/works/MC.jpg'), PosixPath('/home/works/workspace.yaml'), PosixPath('/home/works/Filebrowser.png'), PosixPath('/home/works/Cronicle.jpg')]
    yml_file = get_workspace_yaml(files)
    assert yml_file == PosixPath('/home/works/workspace.yaml')

def test_get_workspace_yml():
    """ Test that workspace yml file is found
    """
    files = [PosixPath('/home/works/IDE_copy.jpg'), PosixPath('/home/works/Htop.jpg'), PosixPath('/home/works/MC.jpg'), PosixPath('/home/works/workspace.yml'), PosixPath('/home/works/Filebrowser.png'), PosixPath('/home/works/Cronicle.jpg')]
    yml_file = get_workspace_yaml(files)
    assert yml_file == PosixPath('/home/works/workspace.yml')

def test_valid_image_extension():
    """ Check that only valid image extensions are allowed
    """
    assert valid_image_extension('/home/works/Htop.jpg'), "JPG image is allowed"
    assert valid_image_extension('/home/works/Htop.png'), "PNG image is allowed"
    assert valid_image_extension('/home/works/Htop.svg'), "SVG image is allowed"
    assert not valid_image_extension('/home/works/Htop.gif'), "GIF image is not allowed"

def test_get_ui_images():
    """ Check that gui images are selected
    """
    wrk_params = read_test_conf('workspace-correct.yaml')
    required_images = get_ui_images(wrk_params)
    assert required_images == ['white-icon.svg', 'dark-icon.svg', 'redis-commander.png', 'blast-radius.png', 'ara.png']

def test_check_images_present():
    """ Should pass because all required images are present
    """
    wrk_params = {'name': 'My workspace', 'doc_url': 'link to the documentation page', 'about': '# Workspace for my work. \nPortable containerized development environment for awesome challenges\n*(created by authentic-apostol, authentic.apostol@gmail.com)*\n', 'logo': 'white-icon.svg', 'favicon': 'dark-icon.svg', 'styles': {'font': 'Roboto', 'colors': {'light': {'primary': '#252525', 'accent': '#19758F', 'background': '#F5F7F7'}, 'dark': {'primary': '#3C3C3C', 'accent': '#E77260', 'background': '#1E1E1E', 'title': '9CDCFE', 'text': '9CDCFE'}}}, 'pages': {'home': [{'name': 'REDIS_COMMANDER', 'port': 8032, 'path': '/', 'title': 'Redis Commander', 'description': 'Redis web management tool', 'image': 'redis-commander.png'}], 'admin': [{'name': 'BlAST_RADIUS', 'port': 8033, 'title': 'Blast Radius', 'description': 'Schedule jobs, manage schedules, observe and monitor executions', 'image': 'Blast-radius.png'}], 'my_apps': [{'name': 'ANSIBLE_ARA', 'port': 8031, 'title': 'Ansible Ara', 'description': 'Monitor Ansible plays', 'image': 'ara.png'}]}, 'start': [{'name': 'ANSIBLE_ARA', 'cmd': 'ara-manage runserver 0.0.0.0:8031'}, {'name': 'CRONICLE', 'dir': '/opt/cronicle', 'cmd': 'rm /opt/cronicle/logs/cronicled.pid || true; cd /opt/cronicle; . env/bin/activate; /opt/cronicle/bin/control.sh setup; /opt/cronicle/bin/control.sh start'}, {'name': 'REDIS_COMMANDER', 'dir': '/opt/redis-commander', 'cmd': '. env/bin/activate && redis-commander --port=8029'}]}
    files = [PosixPath('/home/works/white-icon.svg'), PosixPath('/home/works/dark-icon.svg'), PosixPath('/home/works/redis-commander.png'), PosixPath('/home/works/ara.png'), PosixPath('/home/works/Blast-radius.png'), PosixPath('/home/works/workspace.yaml'), PosixPath('/home/works/Filebrowser_copy.png'), PosixPath('/home/works/Cronicle.jpg')]
    assert check_images_present(wrk_params, files), "All images must be present"
    
def test_check_images_missing(): 
    """ Should fail because of missing images
    """
    wrk_params = {'name': 'My workspace', 'doc_url': 'link to the documentation page', 'about': '# Workspace for my work. \nPortable containerized development environment for awesome challenges\n*(created by authentic-apostol, authentic.apostol@gmail.com)*\n', 'logo': 'white-icon.svg', 'favicon': 'dark-icon.svg', 'styles': {'font': 'Roboto', 'colors': {'light': {'primary': '#252525', 'accent': '#19758F', 'background': '#F5F7F7'}, 'dark': {'primary': '#3C3C3C', 'accent': '#E77260', 'background': '#1E1E1E', 'title': '9CDCFE', 'text': '9CDCFE'}}}, 'pages': {'home': [{'name': 'REDIS_COMMANDER', 'port': 8032, 'path': '/', 'title': 'Redis Commander', 'description': 'Redis web management tool', 'image': 'redis-commander.png'}], 'admin': [{'name': 'BlAST_RADIUS', 'port': 8033, 'title': 'Blast Radius', 'description': 'Schedule jobs, manage schedules, observe and monitor executions', 'image': 'Blast-radius.png'}], 'my_apps': [{'name': 'ANSIBLE_ARA', 'port': 8031, 'title': 'Ansible Ara', 'description': 'Monitor Ansible plays', 'image': 'ara.png'}]}, 'start': [{'name': 'ANSIBLE_ARA', 'cmd': 'ara-manage runserver 0.0.0.0:8031'}, {'name': 'CRONICLE', 'dir': '/opt/cronicle', 'cmd': 'rm /opt/cronicle/logs/cronicled.pid || true; cd /opt/cronicle; . env/bin/activate; /opt/cronicle/bin/control.sh setup; /opt/cronicle/bin/control.sh start'}, {'name': 'REDIS_COMMANDER', 'dir': '/opt/redis-commander', 'cmd': '. env/bin/activate && redis-commander --port=8029'}]} 
    files = [PosixPath('/home/works/IDE_copy.jpg'), PosixPath('/home/works/Htop_copy.jpg'), PosixPath('/home/works/MC_copy.jpg'), PosixPath('/home/works/workspace.yaml'), PosixPath('/home/works/Filebrowser_copy.png'), PosixPath('/home/works/Cronicle.jpg')]
    with pytest.raises(Exception) as e:
        check_images_present(wrk_params, files)
    assert e.type == Exception, "some images must be missing"

def test_proper_dir():
    """ Test the correct config folder
    """
    conf_dir_path = get_full_conf_dir_path("correct")
    assert read_conf_dir(conf_dir_path) is not None, "Should be the correct config dir"

def test_conf_dir_missing_image():
    """ Test the config folder with a missing image
    """
    conf_dir_path = get_full_conf_dir_path("missing-icon")
    with pytest.raises(Exception) as e:
        read_conf_dir(conf_dir_path)
    assert e.type == Exception, "There are some images missing in the config dir"