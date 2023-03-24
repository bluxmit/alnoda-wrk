""" Module to install applications from alnoda.org
"""
import os, shutil
import socket
import requests
import subprocess
from packaging import version as Version
import typer
from .globals import clnstr, WORKSPACE_DIR
from .fileops import read_ui_conf, update_ui_conf, read_lineage
from .ui_builder import copy_pageapp_image
from .alnoda_api import AlnodaApi, AlnodaSignedApi
from .wrk_supervisor import create_supervisord_file
from .fileops import read_ui_conf, update_ui_conf, read_meta
from .meta_about import update_meta, refresh_from_meta, app_already_installed, log_app_installed, get_workspace_id, is_port_in_app_use

APP_INSTALL_TEMP_LOC = '/tmp/instl'
ALLOWED_FREE_PORT_RANGE_MIN = 8031
ALLOWED_FREE_PORT_RANGE_MAX = 8040
DEFAULT_APP_INSTALL_PAGE = 'home'


class AlnodaApiApp(AlnodaApi):
    def __init__(self, what, **kwargs):
        app_code = kwargs['app_code']
        if what == 'meta':
            if 'version' in kwargs:  
                version = kwargs['version']
                path = f'app/{app_code}/{version}/meta/'
            else:  path = f'app/{app_code}/meta/'
        elif what == 'compatibility':
            version_code = kwargs['version_code']
            path = f'app/{app_code}/{version_code}/compat/'
        super().__init__(path)


def get_free_ports():
    """ Check if workspace has free ports, and return one of them """
    ui_conf = read_ui_conf()
    # what ports are already taken:
    taken_ports = []
    for page in ui_conf.keys():
        page_data = ui_conf[page]
        for app,adic in page_data.items():
            if 'port' in adic: taken_ports.append(adic['port'])
    # determine free ports
    free_ports = []
    for p in range(ALLOWED_FREE_PORT_RANGE_MIN, ALLOWED_FREE_PORT_RANGE_MAX+1):
        if p not in taken_ports:
            free_ports.append(p)
    return free_ports


def check_compatibility(app_code, version_code, version):
    """ Fetch app version compatibility and reconcile with this workspace legacy """
    api_comp = AlnodaApiApp('compatibility', app_code=app_code, version_code=version_code)
    res, app_compat = api_comp.fetch()
    if res is False: return False
    if 'all_workspaces' in app_compat or len(app_compat)==0: return True
    # if there are defined compatibilities rules, fetch workspace lineage
    lineage = read_lineage()
    lineage_dict = {e['name']:e for e in lineage}
    app_compat_dict = {e['workspace_name']:e for e in app_compat}
    # compare 
    for w,d in app_compat_dict.items():
        # find if any of app compatible workspaces is present in the workspace lineage
        if w in lineage_dict.keys():
            # check versions match
            this = lineage_dict[w]
            required_geq = d['required_geq']
            required_leq = d['required_leq']
            if str(version) == str(required_geq) or str(version) == str(required_leq):
                return True
            this_version = Version.parse(str(this['version']))
            compatible = True
            if len(str(required_geq)) > 0:
                required_geq_version = Version.parse(required_geq)
                if this_version < required_geq_version: compatible = False
            if len(str(required_leq)) > 0:
                required_required_leq = Version.parse(required_leq)
                if this_version > required_required_leq: compatible = False
            return compatible
    return False


def make_apinstall_temp_dir(app_code):
    """ make sure temporary folder for installation artifacts exists """
    # make sure temp folder for this app exist, and it is new
    if not os.path.exists(APP_INSTALL_TEMP_LOC): os.makedirs(APP_INSTALL_TEMP_LOC)
    app_temp_dir = os.path.join(APP_INSTALL_TEMP_LOC, app_code)
    # just inn case, delete if this app_temp_dir already exist
    if shutil.os.path.exists(app_temp_dir): shutil.rmtree(app_temp_dir)
    # create this folder anew
    os.makedirs(app_temp_dir)
    return app_temp_dir


def install_app(app_meta, install_temp_dir):
    """ Install application using install script """
    install_script = clnstr(app_meta['install_script'])
    require_terminal_restart = False
    if 'wrk' in install_script and 'alias' in install_script: require_terminal_restart = True
    # save install script there
    script_path = os.path.join(install_temp_dir, 'install.sh')
    with open(script_path, 'w') as f:
        f.write(install_script)
    os.chmod(script_path, 0o755)
    # install applicationn and its dependencies using the script
    result = subprocess.run(['bash', script_path], capture_output=True, text=True)
    return result, require_terminal_restart


def is_os_port_in_use(port):
    """ Simply check if port is free """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('0.0.0.0', port)) == 0


def add_app(app_code, version=None, silent=False):
    """ Install app locally """
    # check app is not already installed
    if app_already_installed(app_code):
        if not silent: typer.echo("app already installed")
        return
    # fetch app version
    if version is not None: 
        api = AlnodaApiApp('meta', app_code=app_code, version=version)
    else:
        api = AlnodaApiApp('meta',app_code=app_code)
    res, app_meta = api.fetch()
    if res is False:
        if not silent: typer.echo("App or app version not found")
        return False, "App or app version not found"
    if not silent: typer.echo("starting...")
    version_id = app_meta['version_id']
    version_code = app_meta['version_code']
    version = app_meta['version']
    app_name = app_meta['name']
    app_desctiption = app_meta['description']
    ### check compatibility
    if not silent: 
        typer.echo("checking compatibility...")
        is_compatible = check_compatibility(app_code, version_code, version)
        if not is_compatible:
            typer.echo("WARNING: This app is not explicitly compatible the workspace lineage")
            should_continue = typer.confirm("Do you want to continue?")
            if not should_continue: return
    ### Check if app exposes UI and wrkspace has free ports
    app_has_UI = False
    if 'app_port' in app_meta and app_meta['app_port'] is not None and app_meta['app_port'] != 'None' and len(str(app_meta['app_port']))>0:
        app_has_UI = True; port_correct = True
        # first check that port is int
        try: 
            app_port = int(app_meta['app_port'])
            # then check port is within a proper port range
            if app_port <= 0 or app_port >= 65535: port_correct = False
        except: app_has_UI = False; port_correct = False
        if not port_correct:
            if not silent: 
                typer.echo("Application UI port is misconfigured!")
                typer.echo("Installation FAILED")
            return
        # now check port is free
        if is_os_port_in_use(app_port) or is_port_in_app_use(port): 
            if not silent: 
                typer.echo(f"Application listens to port {app_port}, but it is already in use")
                typer.echo("Installation FAILED")
            return
    if app_has_UI:
        if not silent: typer.echo("assigning port...")
        app_port = app_meta['app_port']
        free_ports = get_free_ports()
        # if app has UI, but workspace has no free ports - stop here
        if len(free_ports) == 0:
            return False, "Limit of applications with UI reached"
        # prescribe first free port to the app
        prescribed_port = free_ports[0]
        # if app port is one of the free ports, take it
        if app_port in free_ports:
            prescribed_port = app_port
    ### Folder for install artefacts
    install_temp_dir = make_apinstall_temp_dir(app_code)
    ### Install app using the script
    if not silent: typer.echo("running install script...")
    install_result, require_terminal_restart = install_app(app_meta, install_temp_dir)
    if not silent: typer.echo(install_result)
    ### Add startup script
    app_should_run_as_daemon = False
    if 'start_script' in app_meta and app_meta['start_script'] is not None and app_meta['start_script'] != 'None' and len(str(app_meta['start_script']))>0:
        app_should_run_as_daemon = True
    if app_should_run_as_daemon:
        if not silent: typer.echo("setting startup configuration...")
        start_script = clnstr(app_meta['start_script'])
        create_supervisord_file(name=app_code, cmd=start_script, folder=None, env_vars=None)
        if not silent: 
            typer.echo("-------------------------------------------------------------")
            typer.echo("---- application will start after workspace is restarted ----")
            typer.echo("-------------------------------------------------------------")
    ### Add UI
    app_port = None
    if app_has_UI:
        if not silent: typer.echo("updating workspace UI...")
        # do we need port-mapping?
        if prescribed_port != app_port:
            socat_cmd = f"socat tcp-listen:{prescribed_port},reuseaddr,fork tcp:localhost:{app_port}"
            create_supervisord_file(name=f'{app_code}-soc', cmd=socat_cmd, folder=None, env_vars=None)
        # copy image from S3
        ui_page = DEFAULT_APP_INSTALL_PAGE
        img_loc_prefix = ""
        if ui_page == 'home': img_loc_prefix = "assets/home/"
        image_url = app_meta['image_url']
        img_response = requests.get(image_url)
        img_content = img_response.content
        img_name = f'{app_code}.webp'
        image_path = os.path.join(install_temp_dir, img_name)
        with open(image_path, 'wb') as f:
            f.write(img_content)
        copy_pageapp_image(ui_page, image_path)
        # add UI shortcut to the workspace dashboard
        ui_conf = read_ui_conf()
        page_conf = ui_conf[ui_page]
        ui_dict = {
            'title': app_meta['name'],
            'port': prescribed_port,
            'description': app_meta['description'],
            'image': f'{img_loc_prefix}{img_name}'
        }
        if 'ui_path' in app_meta and app_meta['ui_path'] is not None and app_meta['ui_path'] != 'None' and len(str(app_meta['ui_path']))>0:
            ui_path = app_meta['ui_path'] 
            if ui_path[0] == "/": 
                ui_path = ui_path[1:]
            ui_dict['path'] = ui_path
        page_conf[app_code] = ui_dict
        update_ui_conf(ui_conf)
    ### Add workspace tags
    if 'tags' in app_meta:  
        if not silent: typer.echo("adding workspace tags...")
        app_tags = app_meta['tags']
        try:
            new_meta = read_meta()
            new_meta['tags'] = new_meta['tags'] + ', '.join(app_tags)
            update_meta(name=new_meta['name'], version=new_meta['version'], author=new_meta['author'], docs=new_meta['docs'], tags=new_meta['tags'])
            refresh_from_meta()
        except: pass
    ### log installed app to meta 
    log_app_installed(app_code, name=app_name, version=version, desctiption=app_desctiption, app_port=app_port)
    ### if auth token is present - log to alnoda.org
    s_api = AlnodaSignedApi("workspace/history/add/app/")
    success, result = s_api.fetch(data = {'app_data': {app_code:  {'app_code': app_code, 'app_name': app_name, 'version_code': version_code, 'app_version': version}}})
    if not success:
        error = result['error']
        if not silent: typer.echo(f"could not update workspace app history at alnoda.org: {error}")
    ### Done!
    if require_terminal_restart:
        if not silent: typer.echo("---- RESTART TERMINAL TO APPLY CHANGES ----")
    if not silent: typer.echo("done")

