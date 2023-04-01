""" Module to install applications from alnoda.org
"""
import os, shutil
import socket
import requests
import subprocess
from packaging import version as Version
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
from .globals import clnstr, WORKSPACE_DIR
from .fileops import read_ui_conf, update_ui_conf, read_lineage
from .ui_builder import copy_pageapp_image
from .alnoda_api import AlnodaApi, AlnodaSignedApi
from .wrk_supervisor import create_supervisord_file
from .fileops import read_ui_conf, update_ui_conf, read_meta
from .meta_about import update_meta, refresh_from_meta, app_already_installed, log_app_installed, get_workspace_id, is_port_in_app_use

INSTALL_PID_FILE = '/tmp/app-install.pid'
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
    if res is False: return False, "Workspace compatibility of this app is wrongly defined", False, "App compatibility of this app is wrongly defined"
    workspaces_compatibility = []
    if 'workspaces' in app_compat: workspaces_compatibility = app_compat['workspaces']
    apps_compatibility = []
    if 'apps' in app_compat: apps_compatibility = app_compat['apps']
    # define compatibility markers
    wrk_compatible = True
    wrk_compatibility_message = ""
    app_compatible = True
    app_compatibility_message = ""
    # check workspace compatibility
    if len(workspaces_compatibility) > 0:
        lineage = read_lineage()
        lineage_dict = {e['name']:e for e in lineage}
        workspaces_compatibility_dict = {e['workspace_name']:e for e in workspaces_compatibility}
        for w,d in workspaces_compatibility_dict.items():
            # find if any of app compatible workspaces is present in the workspace lineage
            if w in lineage_dict.keys():
                # check versions match
                this = lineage_dict[w]
                required_geq = d['required_geq']
                required_leq = d['required_leq']
                this_version_ = str(this['version'])
                this_version = Version.parse(this_version_)
                if required_geq is not None and len(str(required_geq)) > 0:
                    required_geq_version = Version.parse(required_geq)
                    if this_version < required_geq_version: 
                        wrk_compatible = False
                        wrk_compatibility_message = f"App requires workspace {w} version greater or equal {required_geq}. This workspace lineage has {w} version {this_version_}"
                if required_leq is not None and len(str(required_leq)) > 0:
                    required_required_leq = Version.parse(required_leq)
                    if this_version > required_required_leq: 
                        wrk_compatible = False
                        wrk_compatibility_message = f"App requires workspace {w} version smaller or equal {required_leq}. This workspace lineage has {w} version {this_version_}"
    if len(apps_compatibility) > 0:
        meta = read_meta()
        this_app_dict = {}
        try: this_app_dict = meta['alnoda.org.apps']
        except: pass
        has_compatibles_list = False; satisfies_compatibles_list = False  # if there re rules of type 'compatible'
        apps_compatibility_dict = {e['another_app']:e for e in apps_compatibility}
        for a,d in apps_compatibility_dict.items():
            compatibility_type = d['compatibility_type']
            required_geq = d['required_geq']
            required_leq = d['required_leq']
            if required_geq is not None and len(str(required_geq)) > 0: required_geq_version = Version.parse(required_geq)
            if required_leq is not None and len(str(required_leq)) > 0: required_required_leq = Version.parse(required_leq)
            if a not in this_app_dict:
                if compatibility_type == 'requires':
                    app_compatible = False
                    app_compatibility_message = f"This app requires another app (id) {a}, but it is not installed in this workspace. Check out compatible version at alnoda.org"
            else:
                this = this_app_dict[a]
                this_version_ = str(this['version'])
                this_version = Version.parse(this_version_)
                if compatibility_type in ['requires']:
                    if required_geq is not None and len(str(required_geq))>0:
                        if this_version < required_geq_version: 
                            app_compatible = False
                            app_compatibility_message = f"This app requires another app (id) {a} version greater or equal {required_geq}, but this workspace has version {this_version_} of the required app"
                        else: satisfies_compatibles_list = True
                    if required_leq is not None and len(str(required_leq))>0:
                        if this_version > required_required_leq: 
                            app_compatible = False
                            app_compatibility_message = f"This app requires another app (id) {a} version smaller or equal {required_leq}, but this workspace has version {this_version_} of the required app"
                        else: satisfies_compatibles_list = True
                elif compatibility_type in ['compatible']:
                    has_compatibles_list = True
                    if (required_geq is not None and len(str(required_geq))>0) and (required_leq is not None and len(str(required_leq))>0):
                        if (this_version > required_geq_version) and (this_version < required_required_leq): 
                            satisfies_compatibles_list = True
                    elif required_geq is not None and len(str(required_geq))>0:
                        if this_version > required_geq_version: 
                            satisfies_compatibles_list = True
                    elif required_leq is not None and len(str(required_leq))>0:
                        if this_version < required_required_leq: 
                            satisfies_compatibles_list = True
                    elif (required_geq is None or len(str(required_geq))==0) and (required_leq is None or len(str(required_leq))==0):
                        satisfies_compatibles_list = True # <- compatible with all versions
                elif compatibility_type in ['incompatible']:
                    if required_geq is not None and  len(str(required_geq))>0:
                        if this_version >= required_geq_version: 
                            app_compatible = False
                            app_compatibility_message = f"This app is incompatible with app (id) {a} version greater or equal {required_geq}, and this workspace has version {this_version_} of this app"
                    if required_leq is not None and len(str(required_leq))>0:
                        if this_version <= required_required_leq:
                            app_compatible = False
                            app_compatibility_message = f"This app is incompatible with app (id) {a} version smaller or equal {required_leq}, and this workspace has version {this_version_} of this app"
                    if (required_geq is None or len(str(required_geq))==0) and (required_leq is None or len(str(required_leq))==0):
                        app_compatible = False
                        app_compatibility_message = f"This app is incompatible with all versions of app (id) {a}, and this workspace has this app installed"
        if app_compatible and has_compatibles_list == True and satisfies_compatibles_list == False:
            app_compatible = False
            app_compatibility_message = f"This app has a list of compatible apps and versions, but this workspace has none of those installed"
    return wrk_compatible, wrk_compatibility_message, app_compatible, app_compatibility_message


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


def add_app_tags_to_wrk(app_meta):
    """ Add application tags to the workspace tags """
    try:
        app_tags_set = set(app_meta['tags'])
        wrk_meta = read_meta()
        wrk_tags_ = wrk_meta['tags'].split(",")
        wrk_tags = [t.strip().replace(" ","") for t in wrk_tags_]
        wrk_tags_set = set(wrk_tags)
        new_wrk_tags_set = wrk_tags_set.union(app_tags_set)
        new_wrk_tags_list = list(new_wrk_tags_set)
        new_wrk_tags = ", ".join(new_wrk_tags_list)
        update_meta(tags=new_wrk_tags)
        refresh_from_meta()
    except: pass


def add_app(app_code, version=None, silent=False):
    """ Install app locally """
    # check app is not already installed
    if app_already_installed(app_code):
        if not silent: typer.echo("✅ app already installed")
        return
    # ensure only one installation at a time
    if os.path.isfile(INSTALL_PID_FILE):
        if not silent: 
            typer.echo("🛑 Another app is being installed right now. Please install only one app at a time!")
            typer.echo(f"(if this is an error, remove pid file with 'rm {INSTALL_PID_FILE}')")
        return
    with open(INSTALL_PID_FILE, 'w', encoding='utf-8') as f:
        f.write(str(os.getpid()))
    # Wrap entire installation in try-except-finally
    try:
        # fetch app version
        if version is not None: 
            api = AlnodaApiApp('meta', app_code=app_code, version=version)
        else:
            api = AlnodaApiApp('meta',app_code=app_code)
        res, app_meta = api.fetch()
        if res is False:
            if not silent: typer.echo("🛑 App or app version not found")
            return 
        if not silent: 
            typer.echo("✨ starting...")
            typer.echo("⚠️ Please DO NOT close this terminal window untill app is fully installed!")
        version_id = app_meta['version_id']
        version_code = app_meta['version_code']
        version = app_meta['version']
        app_name = app_meta['name']
        app_desctiption = app_meta['description']
        ### check if install script has recursive installation with alnoda-wrk (we need to delete INSTALL_PID_FILE THEN)
        if 'wrk' in app_meta['install_script'] and 'install' in app_meta['install_script']:
            if os.path.exists(INSTALL_PID_FILE): os.remove(INSTALL_PID_FILE)
        ### check compatibility (it is optional, so wrap in try-except)
        if not silent: 
            # try:
            typer.echo("➡️ checking compatibility...")
            wrk_compatible, wrk_compatibility_message, app_compatible, app_compatibility_message = check_compatibility(app_code, version_code, version)
            if not wrk_compatible:
                typer.echo(f"⚠️ WARNING: {wrk_compatibility_message}")
                should_continue = typer.confirm("Do you want to continue❓")
                if not should_continue: return
            if not app_compatible:
                typer.echo(f"⚠️ WARNING: {app_compatibility_message}")
                should_continue = typer.confirm("Do you want to continue❓")
                if not should_continue: return
            # except: pass
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
                    typer.echo("🛑 Application UI port is misconfigured!")
                    typer.echo("😢 Sorry cannot continue!")
                return
            # now check port is free
            if is_os_port_in_use(app_port) or is_port_in_app_use(app_port): 
                if not silent: 
                    typer.echo(f"Application listens to port {app_port}, but it is already in use")
                    typer.echo("Installation FAILED")
                return
        if app_has_UI:
            if not silent: typer.echo("➡️ assigning port...")
            app_port = app_meta['app_port']
            free_ports = get_free_ports()
            # if app has UI, but workspace has no free ports - stop here
            if len(free_ports) == 0:
                typer.echo("😢 Sorry, the limit of 10 applications with UI reached")
                return False, "✋ Limit of applications with UI reached"
            # prescribe first free port to the app
            prescribed_port = free_ports[0]
            # if app port is one of the free ports, take it
            if app_port in free_ports:
                prescribed_port = app_port
        ### Folder for install artefacts
        install_temp_dir = make_apinstall_temp_dir(app_code)
        ### Install app using the script
        if not silent:
            typer.echo("➡️ executing installation script...")
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(description="installing... ...", total=None)
                install_result, require_terminal_restart = install_app(app_meta, install_temp_dir)
            print("✔️ app installed")
        else: install_result, require_terminal_restart = install_app(app_meta, install_temp_dir)
        # if not silent: typer.echo(install_result)
        ### Add startup script
        app_should_run_as_daemon = False
        if 'start_script' in app_meta and app_meta['start_script'] is not None and app_meta['start_script'] != 'None' and len(str(app_meta['start_script']))>0:
            app_should_run_as_daemon = True
        if app_should_run_as_daemon:
            if not silent: typer.echo("➡️ setting startup configuration...")
            start_script = clnstr(app_meta['start_script'])
            create_supervisord_file(name=app_code, cmd=start_script, folder=None, env_vars=None)
            if not silent: 
                typer.echo("-------------------------------------------------------------")
                typer.echo("- ⚠️ application will start after workspace is restarted ⚠️  -")
                typer.echo("-------------------------------------------------------------")
        ### Add UI
        if app_has_UI:
            if not silent: typer.echo("➡️ updating workspace UI...")
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
            if not silent: typer.echo("➡️ adding workspace tags...")
            add_app_tags_to_wrk(app_meta)
        ### log installed app to meta
        try: log_app_installed(app_code, name=app_name, version=version, desctiption=app_desctiption, app_port=app_port) # when app has UI (app_port is defined)
        except: log_app_installed(app_code, name=app_name, version=version, desctiption=app_desctiption) # when app does not have UI (app_port is NOT defined)
        ### if auth token is present - log to alnoda.org
        s_api = AlnodaSignedApi("workspace/history/add/app/")
        success, result = s_api.fetch(data = {'app_data': {app_code:  {'app_code': app_code, 'app_name': app_name, 'version_code': version_code, 'app_version': version}}})
        if not success:
            error = result['error']
            if not silent: typer.echo(f"❗ Could not update workspace app history at alnoda.org: {error}")
        ### Done!
        if not silent and require_terminal_restart: typer.echo("---- ⚠️ RESTART TERMINAL REQUIRED TO APPLY CHANGES ----")
        if not silent: 
            typer.echo("✍️ If app is not working try restarting terminal window or entire workspace")
            typer.echo("🚀 done")
        # If remarks are present, display (optional, enclose in try-except)
        try:
            if not silent and 'remarks' in app_meta and app_meta['remarks'] is not None and len(str(app_meta['remarks']))>0:
                remarks = app_meta['remarks']
                typer.echo("***********************************************")
                typer.echo(remarks)
                typer.echo("***********************************************")
        except: pass
    # except entire installation failed
    except:
        if not silent: typer.echo("🛑 Sorry, there was an error. Installation could fail or application might not work correctly")
    finally: 
        if os.path.exists(INSTALL_PID_FILE): os.remove(INSTALL_PID_FILE)
    return

