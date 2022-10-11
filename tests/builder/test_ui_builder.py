import pytest
from unittest.mock import patch
from pathlib import Path
from alnoda_wrk.conf_parser import *
from alnoda_wrk.ui_builder import *
from alnoda_wrk.globals import safestring
import yaml, json
import os, shutil
from datetime import date
from ..conf_parse.test_config_dir import get_full_conf_dir_path


def mock_globals(monkeypatch, kdir="/tmp"):
    """
    """
    mgl = ["globals", "meta_about", "conf_parser", "ui_builder", "builder", "fileops", "wrk_supervisor"]
    for m in mgl:
        try: monkeypatch.setattr(f"alnoda_wrk.{m}.HOME_DIR", f"{kdir}/")
        except: pass
        try: monkeypatch.setattr(f"alnoda_wrk.{m}.WORKSPACE_DIR", f"{kdir}/.wrk")
        except: pass
        try: monkeypatch.setattr(f"alnoda_wrk.{m}.WORKSPACE_UI_DIR", f"{kdir}/.wrk/ui")
        except: pass
        try: monkeypatch.setattr(f"alnoda_wrk.{m}.WORKSPACE_META_FILE", f"{kdir}/.wrk/meta.json")
        except: pass
        try: monkeypatch.setattr(f"alnoda_wrk.{m}.MKDOCS_ASSETS_DIR", f"{kdir}/.wrk/ui/docs/assets")
        except: pass
        try: monkeypatch.setattr(f"alnoda_wrk.{m}.mkdocs_assets_dir", f"{kdir}/.wrk/ui/docs/assets")
        except: pass
        try: monkeypatch.setattr(f"alnoda_wrk.{m}.WORKSPACE_UI_SCSS_STYLES_FILE", f"{kdir}/.wrk/ui/docs/stylesheets/extra.css")
        except: pass
        try: monkeypatch.setattr(f"alnoda_wrk.{m}.WORKSPACE_ABOUT_FILE", f"{kdir}/.wrk/ui/docs/about.md")
        except: pass  
        try: monkeypatch.setattr(f"alnoda_wrk.{m}.mkdocs_yml_path", f"{kdir}/.wrk/ui/mkdocs.yml")
        except: pass
        try: monkeypatch.setattr(f"alnoda_wrk.{m}.mkdocs_extra_css_path", f"{kdir}/.wrk/ui/docs/stylesheets/extra.css")
        except: pass
        try: monkeypatch.setattr(f"alnoda_wrk.{m}.ui_dict_file", f"{kdir}/.wrk/ui/conf/ui-apps.json")
        except: pass
        try: monkeypatch.setattr(f"alnoda_wrk.{m}.mkdocs_home_page_assets_dir", f"{kdir}/.wrk/ui/docs/assets")
        except: pass
        try: monkeypatch.setattr(f"alnoda_wrk.{m}.mkdocs_other_page_assets_dir", f"{kdir}/.wrk/ui/docs/pages")
        except: pass
        try: monkeypatch.setattr(f"alnoda_wrk.{m}.SUPERVISORD_FOLDER", f"{kdir}/supervisord")
        except: pass
        try: monkeypatch.setattr(f"alnoda_wrk.{m}.VAR_LOG_FOLDER", f"{kdir}/log")
        except: pass
        try: monkeypatch.setattr(f"alnoda_wrk.{m}.WORKSPACE_LINEAGE_FILE", f"{kdir}/.wrk/lineage.json")
        except: pass
    return


def test_init_wrk(monkeypatch):
    """ test that workspace is initiated in the proper folder """
    # MOCK
    mock_globals(monkeypatch)
    from alnoda_wrk import builder
    from alnoda_wrk.meta_about import read_meta 
    # TEST
    builder.init_wrk()
    # assert folder is initialized
    assert os.path.isdir("/tmp/.wrk"), "Workspace must be initialised"
    # assert meta refreshed with today's date
    m = read_meta()
    assert str(m['created']) == str(date.today()), "Meta should have today's date"
    # check subfolders and files were created
    assert os.path.isdir("/tmp/.wrk/ui"), "UI folder must be created"
    assert os.path.isdir("/tmp/.wrk/ui/conf"), "ui/conf folder must be created"
    assert os.path.isfile("/tmp/.wrk/ui/mkdocs.yml"), "mkdocs.yml must be copied"
    # clear test results
    shutil.rmtree("/tmp/.wrk")
    return


def test_update_required_ui_params(monkeypatch):
    """ Test that updating of required UI parameters (parsed from the config.yaml) change the meta.json and about.md """
    # MOCK
    conf_dir_path = get_full_conf_dir_path("correct")
    name = 'This test workspace'; doc_url = 'http://this-test-link'; author = 'test-author'; version = 5.11; description = 'Test workspace description'
    wrk_params = {'name': name, 'doc_url': doc_url, 'author': author, 'version': version, 'description': description, 'logo': 'white-icon.svg', 'favicon': 'dark-icon.svg', 'styles': {'font': 'Roboto', 'colors': {'light': {'primary': '#252525', 'accent': '#19758F', 'background': '#F5F7F7'}, 'dark': {'primary': '#3C3C3C', 'accent': '#E77260', 'background': '#1E1E1E', 'title': '#9CDCFE', 'text': '#9CDCFE'}}, 'common_colors': {'header': '#FFFFFF', 'nav': '#eab676'}}} 
    mock_globals(monkeypatch)
    from alnoda_wrk import builder
    from alnoda_wrk.ui_builder import update_required_ui_params, get_mkdocs_yml
    from alnoda_wrk.meta_about import read_meta, read_about 
    # RUN TEST
    builder.init_wrk()
    builder.init_supervisord()
    update_required_ui_params(wrk_params, conf_dir_path)
    # CHECK mkdocs dict
    mkdocs_yml = get_mkdocs_yml()
    assert mkdocs_yml['site_name'] == name, f"The site_name in the mkdocs.yml file was not updated to {name}"
    ydoc = [d for d in mkdocs_yml['nav'] if 'Docs' in d.keys()][0]
    assert ydoc['Docs'] == doc_url, f"The doc url was not updated to {doc_url}"
    # CHECK meta
    meta = read_meta()
    assert meta['name'] == name, f"The name in meta.json was not updated to {name}"
    assert meta['version'] == version, f"The version in meta.json was not updated to {version}"
    assert meta['author'] == author, f"The author in meta.json was not updated to {author}"
    assert meta['description'] == description, f"The description in meta.json was not updated to {description}"
    # CHECK about
    about = read_about()
    assert name in about, f"workspace name {name} was not updated in the about.md"
    assert str(version) in about, f"version {version} was not updated in the about.md"
    assert author in about, f"author {author} was not updated in the about.md"
    assert description in about, f"description {description} was not updated in the about.md"
    # clear test results
    shutil.rmtree("/tmp/.wrk"); shutil.rmtree("/tmp/supervisord")
    return


def test_wrk_build(monkeypatch):
    """ Integration test. Check that UI is fully built from the config folder """
    # MOCK
    mock_globals(monkeypatch)
    from alnoda_wrk import builder
    from alnoda_wrk.meta_about import read_meta, read_about 
    from alnoda_wrk.ui_builder import get_mkdocs_yml
    # TEST
    # # Initialize
    builder.init_wrk()
    builder.init_supervisord()
    conf_dir_path = get_full_conf_dir_path("correct")
    builder.build_workspace(conf_dir_path)
    mkdocs_yml = get_mkdocs_yml()
    # CHECK mkdocks.yml
    assert 'extra_css' in mkdocs_yml, "mkdocs.yml structure broken - no extra_css"
    assert 'nav' in mkdocs_yml and len(mkdocs_yml['nav']) > 1, "mkdocs.yml structure broken, nav"
    # CHECK icons 
    assert mkdocs_yml['theme']['favicon'] == 'assets/dark-icon.svg', "favicon is incorrect in mkdocs.yml"
    assert os.path.isfile("/tmp/.wrk/ui/docs/assets/dark-icon.svg"), "favicon dark-icon.svg must be copied"
    assert mkdocs_yml['theme']['logo'] == 'assets/white-icon.svg', "logo is incorrect in mkdocs.yml"
    assert os.path.isfile("/tmp/.wrk/ui/docs/assets/white-icon.svg"), "logo icon white-icon.svg must be copied"
    # CHECK fonts
    assert 'theme' in mkdocs_yml and 'font' in mkdocs_yml['theme'], f"Font must be present in mkdocs_yml.theme, instead {mkdocs_yml['theme']}" 
    assert 'text' in mkdocs_yml['theme']['font'], f"text must be present in mkdocs_yml.theme.font, instead {mkdocs_yml['theme']['font']}" 
    assert mkdocs_yml['theme']['font']['text'] == "Roboto", f"font was incorrectly set, must be Roboto. Instead {mkdocs_yml}"
    # CHECK css
    css_filepath = "/tmp/.wrk/ui/docs/stylesheets/extra.css"
    assert os.path.isfile(css_filepath), "lextra.css file is missing"
    with open(css_filepath, "r") as f:
        scss = f.read()
    assert "#3C3C3C" in scss, f"Color #3C3C3C is missing in extra.css"
    assert "#252525" in scss, f"Color #252525 is missing in extra.css"
    # CHECK ui ui-apps.json
    ui_apps_filepath = "/tmp/.wrk/ui/conf/ui-apps.json"
    assert os.path.isfile(ui_apps_filepath), "ui-apps.json file is missing"
    with open(ui_apps_filepath) as json_file:
        ui_apps_json = json.load(json_file)
    assert "home" in ui_apps_json, f"Home is missing from the ui-apps.json. Instead {ui_apps_json}"
    assert "my_apps" in ui_apps_json, f"my_apps is missing from the ui-apps.json. Instead {ui_apps_json}"
    assert "admin" in ui_apps_json, f"admin is missing from the ui-apps.json. Instead {ui_apps_json}"
    # CHECK home page
    home_page_filepath = "/tmp/.wrk/ui/docs/README.md"
    assert os.path.isfile(home_page_filepath), f"Home page .md file must be present"
    assert "IDE" in ui_apps_json["home"], f"IDE is missing from the ui-apps.json"
    assert "TERMINAL" in ui_apps_json["home"], f"TERMINAL is missing from the ui-apps.json"
    assert "title" in ui_apps_json["home"]["FILEBROWSER"], f"FILEBROWSER title is missing from the ui-apps.json"
    assert "REDIS_COMMANDER" in ui_apps_json["home"], f"REDIS_COMMANDER was not merged into the ui-apps.json"
    # CHECK meta 
    meta_filepath = "/tmp/.wrk/meta.json"
    assert os.path.isfile(meta_filepath), "File meta.json is missing"
    with open(meta_filepath) as json_file:
        meta_json = json.load(json_file)
    assert "author" in meta_json and meta_json["author"] == "bluxmit", "Author is incorrect in meta.json"
    assert "description" in meta_json and len(meta_json["description"]) > 30, "Description is incorrect in meta.json"
    # CHECK about
    about_filepath = "/tmp/.wrk/ui/docs/about.md"
    assert os.path.isfile(about_filepath), f"About page .md file must be present"
    with open(about_filepath, "r") as f:
        about_md = f.read()
    assert "My workspace" in about_md, "Workspace name is missing from the about.md file"
    assert "bluxmit" in about_md, "Author name is missing from the about.md file"
    # CHECK my_apps page
    assert os.path.isfile("/tmp/.wrk/ui/docs/assets/dark-icon.svg"), "favicon dark-icon.svg must be copied"
    assert "PORT_8030" in ui_apps_json["my_apps"], "PORT_8030 is missing from the ui-apps.json"
    assert "ANSIBLE_ARA" in ui_apps_json["my_apps"], "ANSIBLE_ARA was not merged into the ui-apps.json my-apps"
    # CHECK supervisord
    supervisord_folder = "/tmp/supervisord"
    assert os.path.isdir("/tmp/supervisord"), "Supevisord folder must be created"
    assert os.path.isdir("/tmp/log"), "UI app log folder must be created"
    assert os.path.isfile(f"{supervisord_folder}/{safestring('REDIS_COMMANDER')}.conf"), f"supervisord conf file for REDIS_COMMANDER must be added"
    with open(f"{supervisord_folder}/{safestring('REDIS_COMMANDER')}.conf", "r") as f:
        superv_rediscomm = f.read()
    assert ". env/bin/activate && redis-commander --port=8029" in superv_rediscomm, "Startup command for REDIS_COMMANDER was not added"
    # clear test results
    shutil.rmtree("/tmp/.wrk"); shutil.rmtree("/tmp/supervisord"); shutil.rmtree("/tmp/log");
    return



