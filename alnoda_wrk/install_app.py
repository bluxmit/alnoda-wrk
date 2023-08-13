""" Module to install applications from alnoda.org
"""
import os, shutil
import socket
import requests
import subprocess
from packaging import version as Version
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn
from .globals import clnstr, WORKSPACE_DIR, WORKSPACE_HOME_PAGES
from .fileops import read_ui_conf, update_ui_conf, read_lineage, read_meta
from .ui_builder import copy_pageapp_image
from .alnoda_api import AlnodaApi, AlnodaSignedApi
from .wrk_supervisor import create_supervisord_file
from .meta_about import update_meta, refresh_from_meta, app_already_installed, log_app_installed, get_workspace_id, refresh_about
from .links import add_links_section, add_links_url
from .versioning import parse_version, check_semantic_compatibility, check_range_compatible
from .ports import get_free_ports, is_os_port_in_use, is_port_in_app_use

INSTALL_PID_FILE = '/tmp/app-install.pid'
APP_INSTALL_TEMP_LOC = '/tmp/instl'


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


def check_workspace_compatibility(workspaces_compatibility):
    """  Check if app requirement for the workspaces_compatibility is satisfied """
    wrk_compatible = False; wrk_compatibility_message = f"Could not find workspace in the lineage, which is compatible with this app."
    if len(workspaces_compatibility) == 0: #<- compatible with all workspaces
        return True, "app is compatible with all workspaces"
    else:
        lineage = read_lineage()
        lineage_dict = {e['name']:e for e in lineage}
        for W in workspaces_compatibility:
            Wname = W['workspace_name']
            ctype = W['type']
            if Wname in lineage_dict:
                w = lineage_dict[Wname]
                w_ver = str(w['version'])
                if ctype == 'incompatible': return False, f"app is incompatible with workspaces '{Wname}' (all versions)"
                elif ctype ==  'all':     
                    wrk_compatible=True; wrk_compatibility_message=f"app is compatible with all workspaces '{Wname}'"
                elif ctype ==  "exact" and str(w_ver) == str(W['compatibility']['exact']):
                    wrk_compatible=True; wrk_compatibility_message=f"app is compatible with workspace '{Wname}' version {w_ver}"
                elif ctype == 'semantic':
                    if check_semantic_compatibility(w_ver, compdict = W['compatibility']): wrk_compatible = True; wrk_compatibility_message = f"Compatibility with {Wname} version {w_ver}" 
                elif ctype == 'range':
                    if check_range_compatible(w_ver, compdict = W['compatibility']): wrk_compatible = True; wrk_compatibility_message = f"Compatibility with {Wname} version {w_ver}" 
    return wrk_compatible, wrk_compatibility_message


def get_rd_subtype_compatibility(rd):
    """ Get 2 attributes from the element of the compatible_apps dict """
    rd_subtype = 'all'
    try: 
        rd_subtype = rd['sub_type']
        if rd_subtype is None or len(str(rd_subtype)) == 0: rd_subtype = 'all'
    except: pass
    rd_compatibility = {}
    try:
        rd_compatibility = rd['compatibility'] 
    except: pass
    return rd_subtype, rd_compatibility
            

def check_app_compatibility(apps_compatibility):
    app_compatible = True; app_compatibility_message = ""
    # check workspace compatibility
    if len(apps_compatibility) == 0: return True, "" #<- no compatibility restrictions
    else:
        # fetch this workspace app data
        meta = read_meta()
        this_app_dict = {}
        try: this_app_dict = meta['alnoda.org.apps']
        except: pass
        # First we will check none of the installed apps is incompatible with the app
        incompatible_apps_list = [k['another_app'] for k in apps_compatibility if k['compatibility_type'] == 'incompatible']
        incompatibility_apps = [k for k in this_app_dict.keys() if k in incompatible_apps_list]
        if len(incompatibility_apps) > 0:
            return False, f"This workspace has incompatible app(s): {', '.join(incompatibility_apps)}"
        # Next we will check if the new app has required apps
        required_apps_list = [a for a in apps_compatibility if a['compatibility_type'] == 'requires']
        for rd in  required_apps_list:
            rc = rd['another_app']
            if rc not in this_app_dict.keys(): return False, f"This application requires {rc}, which is not installed in this workspace"
            else:
                a_wer = this_app_dict[rc]['version']
                rd_subtype, rd_compatibility = get_rd_subtype_compatibility(rd)
                if rd_subtype == 'all': continue
                elif rd_subtype == 'exact' and str(rd_compatibility['exact']) != str(a_wer):
                    return False, f"this app requires '{rc}' version {rd_compatibility['exact']}. But you have version {a_wer}"
                elif rd_subtype == 'semantic':
                    if not check_semantic_compatibility(a_wer, compdict=rd_compatibility): 
                        return False, "this app requires a different version of '{rc}'" 
                elif rd_subtype == 'range':
                    if not check_range_compatible(a_wer, compdict=rd_compatibility): 
                        return False, "this app requires a different version of '{rc}'"
        # Finally we will check if the new app has any of the compatible apps
        compatible_apps_list = [a for a in apps_compatibility if a['compatibility_type'] == 'compatible']
        if len(compatible_apps_list) > 0:
            app_compatible = False
            for rd in compatible_apps_list: 
                rc = rd['another_app']
                if rc not in this_app_dict.keys(): continue 
                else:
                    a_wer = this_app_dict[rc]['version']
                    rd_subtype, rd_compatibility = get_rd_subtype_compatibility(rd)
                    if rd_subtype == 'all': app_compatible = True
                    if rd_subtype == 'exact' and str(rd_compatibility['exact']) == str(a_wer):
                        app_compatible = True
                    if rd_subtype == 'semantic' and check_semantic_compatibility(a_wer, compdict=rd_compatibility): 
                        app_compatible = True
                    if rd_subtype == 'range' and check_range_compatible(a_wer, compdict=rd_compatibility): 
                        app_compatible = True
            # if we didn't find any of the compatible apps, return False
            if not app_compatible:
                return False, f"This app has a list of compatible applications and versions. None of the compatible apps (or compatible versions) are found in the workspace"
    return app_compatible, app_compatibility_message


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


def add_app(app_code, version=None, page="home", silent=False):
    """ Install app locally """
    # check app is not already installed
    if app_already_installed(app_code):
        if not silent: typer.echo("✅ app already installed")
        return
    # ensure only one installation at a time
    if os.path.isfile(INSTALL_PID_FILE):
        if not silent: 
            typer.echo("🛑 Another app is being installed right now. Simultaneous installations can harm the workspace!")
            should_continue = typer.confirm("Do you want to continue❓")
            if not should_continue: return
    with open(INSTALL_PID_FILE, 'w', encoding='utf-8') as f:
        f.write(str(os.getpid()))
    # check the page is proper
    if page not in WORKSPACE_HOME_PAGES:
        if not silent: typer.echo(f"🛑 wrong page: {page}. Allowed pages: {', '.join(WORKSPACE_HOME_PAGES)}")
        return
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
        app_description = app_meta['description']
        ### check if install script has recursive installation with alnoda-wrk (we need to delete INSTALL_PID_FILE THEN)
        if 'wrk' in app_meta['install_script'] and 'install' in app_meta['install_script']:
            if os.path.exists(INSTALL_PID_FILE): os.remove(INSTALL_PID_FILE)
        ### check compatibility (it is optional, so wrap in try-except)
        if not silent: 
            res = False; app_compat = {}
            try: 
                api_comp = AlnodaApiApp('compatibility', app_code=app_code, version_code=version_code)
                res, app_compat = api_comp.fetch()
            except: pass
            if not res:
                typer.echo(f"⚠️ WARNING: I could not fetch compatibility information for this app")
                should_continue = typer.confirm("Do you want to continue❓")
                if not should_continue: return
            else:
                try:
                    typer.echo("➡️ checking workspace compatibility...")
                    if 'workspaces' in app_compat: 
                        wrk_compatible, wrk_compatible_msg = check_workspace_compatibility(workspaces_compatibility = app_compat['workspaces'])
                        if not wrk_compatible:
                            typer.echo(f"⚠️ WARNING: {wrk_compatible_msg}")
                            should_continue = typer.confirm("Do you want to continue❓")
                            if not should_continue: return
                except: typer.echo("⚠️ WARNING: could not check workspace compatibility, skipping...")
                try:
                    typer.echo("➡️ checking app compatibility...")
                    if 'apps' in app_compat: 
                        app_compatible, app_compatible_msg = check_app_compatibility(apps_compatibility = app_compat['apps'])
                        if not app_compatible:
                            typer.echo(f"⚠️ WARNING: {app_compatible_msg}")
                            should_continue = typer.confirm("Do you want to continue❓")
                            if not should_continue: return
                except: typer.echo("⚠️ WARNING: could not verify app compatibility, skipping...")
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
                typer.echo("😢 Sorry, the limit of applications with UI is reached")
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
            typer.echo("✔️ app installed")
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
                typer.echo("---       restart workspace with    'wrk kill'             ---")
                typer.echo("-------------------------------------------------------------")
        ### Add UI
        if app_has_UI:
            if not silent: typer.echo("➡️ updating workspace UI...")
            # do we need port-mapping?
            if prescribed_port != app_port:
                socat_cmd = f"socat tcp-listen:{prescribed_port},reuseaddr,fork tcp:localhost:{app_port}"
                create_supervisord_file(name=f'{app_code}-soc', cmd=socat_cmd, folder=None, env_vars=None)
            # copy image from S3
            ui_page = page
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
                'real_port': app_port,
                "host": "0.0.0.0",
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
        ### add links
        doc_url = ''; website = ''; repository_url = ''
        try: doc_url = app_meta['doc_url']
        except: pass
        try: website = app_meta['website']
        except: pass
        try: repository_url = app_meta['repository_url']
        except: pass
        if len(doc_url + website + repository_url) > 0:
            secn = "Installed"
            add_links_section(secn)
            if len(doc_url)>0: add_links_url(secn, doc_url, app_name, 'Documentation')
            if len(website)>0: add_links_url(secn, website, app_name, 'Website')
            if len(repository_url)>0: add_links_url(secn, repository_url, app_name, 'Repository')
        ### log installed app to meta
        try: log_app_installed(app_code, name=app_name, version=version, description=app_description, app_port=app_port) # when app has UI (app_port is defined)
        except: log_app_installed(app_code, name=app_name, version=version, description=app_description) # when app does not have UI (app_port is NOT defined)
        ### if auth token is present - log to alnoda.org
        s_api = AlnodaSignedApi("workspace/history/add/app/")
        success, result = s_api.fetch(data = {'app_data': {app_code:  {'app_code': app_code, 'app_name': app_name, 'version_code': version_code, 'app_version': version}}})
        if not success:
            error = "Loggin is currenntly unavailable at alnoda.org"
            try: error = result['error']
            except: pass
            if not silent: typer.echo(f"❗ Could not update workspace app history at alnoda.org: {error}")
        ### Done!
        refresh_about()
        if not silent and require_terminal_restart: typer.echo("---- ⚠️ RESTART TERMINAL REQUIRED TO APPLY CHANGES ----")
        if not silent: 
            typer.echo("✍️ If app is not working try restarting terminal window or entire workspace")
            typer.echo("🚀 done")
            typer.echo("R E S T A R T    T E R M I N A L    N O W   (CTRL+D) !!!!!!!!")
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
        try: subprocess.Popen("cd /home/project", shell=True, stdout=subprocess.PIPE)
        except: pass
    return

