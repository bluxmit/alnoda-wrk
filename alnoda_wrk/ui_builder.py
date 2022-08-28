""" 
Collection of fucntions to build and update the workspace UI 
in the orkspace folder. Update pages, styles, images, logos etc.
"""
import os 
import shutil
import logging
import json, yaml
from pathlib import Path
from jinja2 import Template
from distutils.dir_util import copy_tree
from .globals import *
from .fileops import * 
from .ui_styles import styles_str
from .templates import app_page_str
from .meta_about import update_meta, refresh_about

mkdocs_extra_css_path = os.path.join(WORKSPACE_UI_DIR, 'docs', 'stylesheets', 'extra.css') 
mkdocs_assets_dir = os.path.join(WORKSPACE_UI_DIR, 'docs', 'assets')
mkdocs_home_page_assets_dir = os.path.join(WORKSPACE_UI_DIR, 'docs', 'assets')
mkdocs_other_page_assets_dir = os.path.join(WORKSPACE_UI_DIR, 'docs', 'pages')


def update_required_ui_params(wrk_params, conf_dir_path):
    """ {}, str ->> 
    Update required ui parameters, such as workspace name

    :param wrk_params: dict with the workspace parameters
    :type wrk_params: dict
    :param conf_dir_path: path to the user's workspace config folder
    :type conf_dir_path: str
    """
    # Extract required workspace parameters
    name = wrk_params["name"]
    version = wrk_params["version"]
    author = wrk_params["author"]
    description = wrk_params["description"]
    doc_url = wrk_params["doc_url"]
    # Fetch existing mkdocs.yml file, make updates and save back
    # name
    mkdocs_dict = get_mkdocs_yml()
    mkdocs_dict["site_name"] = name
    # docs link
    for p in mkdocs_dict["nav"]:
        if 'Docs' in p.keys(): p['Docs'] = doc_url
    update_mkdocs_yml(mkdocs_dict)  # <- update mkdocs.yml now
    # meta & about page
    update_meta(
        name=name, 
        version=version,
        author=author,
        description=description
        ); refresh_about()
    return


def update_optional_ui_params(wrk_params, conf_dir_path):
    """ {}, str ->> 
    Update optional ui parameters, such as workspace home page font

    :param wrk_params: dict with the workspace parameters
    :type wrk_params: dict
    :param conf_dir_path: path to the user's workspace config folder
    :type conf_dir_path: str
    """
    # Extract optional workspace parameters
    ## font
    if 'styles' in wrk_params and 'font' in wrk_params['styles']:
        mkdocs_dict = get_mkdocs_yml()
        if 'font' not in mkdocs_dict['theme']: 
            mkdocs_dict['theme']['font'] = {}
        mkdocs_dict['theme']['font']['text'] = wrk_params['styles']['font']
        update_mkdocs_yml(mkdocs_dict)
    return


def update_logo(wrk_params, conf_dir_path):
    """ {}, str ->> 
    Update existing workspace UI - change logo icon. 
    It checks whether new logo is defined in the wrk_params.
    If yes, uploads the logo file to the respective UI folder, and changes the mkdocs.yml file 

    :param wrk_params: dict with the workspace parameters
    :type wrk_params: dict
    :param conf_dir_path: path to the user's workspace config folder
    :type conf_dir_path: str
    """
    if 'logo' in wrk_params:
        # Update mkdocs.yml
        mkdocs_dict = get_mkdocs_yml()
        mkdocs_dict['theme']['logo'] = os.path.join('assets', wrk_params["logo"])
        update_mkdocs_yml(mkdocs_dict)
        # Copy file
        logo_file = os.path.join(conf_dir_path, wrk_params["logo"])
        shutil.copy2(logo_file, mkdocs_assets_dir)
        logging.debug(f"logo updated from file {logo_file}")
    return


def update_favicon(wrk_params, conf_dir_path):
    """ {}, str ->> 
    Update existing workspace UI - change favicon. 
    It checks whether new favicon is defined in the wrk_params.
    If yes, uploads the favicon file to the respective UI folder, and changes the mkdocs.yml file

    :param wrk_params: dict with the workspace parameters
    :type wrk_params: dict
    :param conf_dir_path: path to the user's workspace config folder
    :type conf_dir_path: str
    """
    if 'favicon' in wrk_params:
        # Update mkdocs.yml
        mkdocs_dict = get_mkdocs_yml()
        mkdocs_dict['theme']['favicon'] = os.path.join('assets', wrk_params["favicon"])
        update_mkdocs_yml(mkdocs_dict)
        # Copy file
        favicon_file = os.path.join(conf_dir_path, wrk_params["favicon"])
        shutil.copy2(favicon_file, mkdocs_assets_dir)
        logging.debug(f"favicon updated from file {favicon_file}")
    return


def update_ui_styles(wrk_params):
    """ {} ->> 
    Update existing workspace UI - change CSS styles

    :param wrk_params: dict with the workspace parameters
    :type wrk_params: dict
    """
    # create dict with style settings
    d_styles = {"light": {}, "dark": {}, "common_colors": {}}
    if 'styles' in wrk_params:
        if 'colors' in wrk_params['styles']:
            d_styles.update(wrk_params['styles']['colors'])
        if 'common_colors' in wrk_params['styles']:
            d_styles.update({'common_colors': wrk_params['styles']['common_colors']})
    if len(d_styles.keys()) > 0:      
        # generate jinja template
        tm = Template(styles_str)
        new_styles = tm.render({'styles': d_styles})
        # save styles to mkdocs stylesheet
        with open(mkdocs_extra_css_path, "w") as styles_file:
            styles_file.write(new_styles)
    return


def update_ui_page_from_wrk_params(ui_apps, wrk_params, page):
    """ {}, {}, str ->> {}
    Updates ui_apps with the new page or new page elemets from the wrk_params.

    :param ui_apps: dict with the current MkDocs pages, fetched from the .wrk dir
    :type ui_apps: dict
    :param wrk_params: dict with the workspace parameters
    :type wrk_params: dict
    :param page: the name of the page to merge from wrk_params into ui_apps
    :type page: str
    """
    plist = wrk_params["pages"][page]
    # reshape plist into dict
    pdict = {}
    for d in plist:
        pdict[d['name']] = {i:d[i] for i in d if i!='name'}
    # if ui_apps does not have this page yet, add it
    if page not in ui_apps.keys():
        ui_apps[page] = {}
    ui_apps[page].update(pdict)
    return ui_apps


def move_page_assets(wrk_params, conf_dir_path, page, page_assets_dir):
    """ {}, str, str, str ->>
    Copy respective assets (images) to the UI folder from the user's config dir

    :param wrk_params: dict with the workspace parameters
    :type wrk_params: dict
    :param conf_dir_path: path to the user's workspace config folder
    :type conf_dir_path: str
    :param page: the name of the page to merge from wrk_params into ui_apps
    :type page: str
    :param page_assets_dir: the folder where assets of the page must be copied into
    :type page: str
    """
    # get list of image files
    imgs = [e['image'] for e in wrk_params['pages'][page]]
    imgs_fullpath = [os.path.join(conf_dir_path, img) for img in imgs]
    # make sure folder to copy images into exists
    imgs_dir = os.path.join(page_assets_dir, page)
    Path(imgs_dir).mkdir(parents=True, exist_ok=True) # <- create if not exists 
    # copy files
    for image in imgs_fullpath:
        shutil.copy2(image, imgs_dir)
    return


def update_home_page(wrk_params, conf_dir_path):
    """ {}, {}, str ->> {}
    Update the Home page, if additional apps were added to this page

    :param wrk_params: dict with the workspace parameters
    :type wrk_params: dict
    :param conf_dir_path: path to the user's workspace config folder
    :type conf_dir_path: str
    """
    # Check if wrk_params have additions to the home page
    if 'pages' in wrk_params and 'home' in wrk_params['pages']:
        logging.info(f"Updating Home page with {','.join([p['name'] for p in wrk_params['pages']['home']])}")
        # move image assets into the proper page asset folder
        move_page_assets(wrk_params, conf_dir_path, 'home', mkdocs_home_page_assets_dir)
        # enrich apps of wrk_params['home'] - prepend 'assets/home/' to the image (important! do this after images move)
        for app in wrk_params['pages']['home']:
            app['image'] = os.path.join("assets", "home", app['image'])
        # update and owerwrite ui_apps
        ui_apps = read_ui_conf() 
        ui_apps = update_ui_page_from_wrk_params(ui_apps, wrk_params, 'home')
        update_ui_conf(ui_apps)
    return


def update_other_pages(wrk_params, conf_dir_path):
    """ {}, {}, str ->> 
    Update other pages, apart of home page and about pages 

    :param wrk_params: dict with the workspace parameters
    :type wrk_params: dict
    :param conf_dir_path: path to the user's workspace config folder
    :type conf_dir_path: str
    """
    if 'pages' in wrk_params:
        other_pages = set(wrk_params['pages'].keys()) - {'home'}
        for another_page in other_pages:
            logging.info(f"Updating {another_page} page with {','.join([p['name'] for p in wrk_params['pages'][another_page]])}")
            # update ui_apps
            ui_apps = read_ui_conf() 
            ui_apps = update_ui_page_from_wrk_params(ui_apps, wrk_params, another_page)
            update_ui_conf(ui_apps)
            # move image assets into the proper page asset folder
            move_page_assets(wrk_params, conf_dir_path, another_page, mkdocs_other_page_assets_dir)
            # make sure .md file exists
            app_page_md_file = os.path.join(mkdocs_other_page_assets_dir, f'{another_page}.md')
            with open(app_page_md_file, "w") as md_file:
                md_file.write(app_page_str.replace('PAGE_NAME_REPLACE', another_page))
            # make sure mkdocs.yml has an entry for the page
            mkdocs_dict = get_mkdocs_yml()
            ptitle = another_page.replace("_"," ").capitalize()
            page_entry = {ptitle: os.path.join('pages', f'{another_page}.md')}
            pd = [p for p in mkdocs_dict['nav'] if ptitle in p.keys()]  #<- does workspace has this page already?
            if len(pd) == 0: 
                mkdocs_dict['nav'].append(page_entry)
                mkdocs_dict['nav'] = sorted(mkdocs_dict['nav'], key=lambda x: WORKSPACE_PAGES_ODER.get(list(x.keys())[0],8))
            update_mkdocs_yml(mkdocs_dict)
    return


def build_wrk_ui(wrk_params, conf_dir_path):
    """ {}, str ->>
    Gets existing UI config and the new user's config. And builds the new UI config,
    which is saved to the workspace UI folder.

    :param wrk_params: dict with the workspace parameters
    :type wrk_params: dict
    :param conf_dir_path: path to the user's workspace config folder
    :type conf_dir_path: str
    """
    # mkdocs.yml 
    update_required_ui_params(wrk_params, conf_dir_path)
    update_optional_ui_params(wrk_params, conf_dir_path)
    # logos
    update_logo(wrk_params, conf_dir_path)
    update_favicon(wrk_params, conf_dir_path)
    # styles
    update_ui_styles(wrk_params)
    # pages
    update_home_page(wrk_params, conf_dir_path)
    update_other_pages(wrk_params, conf_dir_path)
    return