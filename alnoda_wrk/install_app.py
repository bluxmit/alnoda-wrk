""" Module to install applications from alnoda.org
"""
import os, shutil
import requests
import subprocess
from packaging import version as Version
from .globals import WORKSPACE_DIR, ALNODA_API_URL
from .fileops import read_ui_conf, read_lineage
from .alnoda_api import AlnodaApi
import typer

APP_INSTALL_TEMP_LOC = '/tmp/instl'
ALLOWED_FREE_PORT_RANGE_MIN = 8031
ALLOWED_FREE_PORT_RANGE_MAX = 8040


class AlnodaApiApp(AlnodaApi):
    def __init__(self, what, **kwargs):
        app_code = kwargs['app_code']
        if what == 'meta':
            if 'version' in kwargs:  path = f'app/{app_code}/{version}/meta/'
            else:  path = f'app/{app_code}/meta/'
        elif what == 'compatibility':
            version_id = kwargs['version_id']
            path = f'app/{app_code}/{version_id}/compat/'
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


def install_app(app_meta):
    """ Install application using install script """
    install_script = app_meta['install_script']
    # make sure temp folder for this app exist, and it is new
    if not os.path.exists(APP_INSTALL_TEMP_LOC): os.makedirs(APP_INSTALL_TEMP_LOC)
    app_temp_dir = os.path.join(APP_INSTALL_TEMP_LOC, app_code)
    # just inn case, delete if this app_temp_dir already exist
    if shutil.os.path.exists(app_temp_dir): shutil.rmtree(app_temp_dir)
    # create this folder anew
    os.makedirs(app_temp_dir)
    # save install script there
    script_path = os.path.join(app_temp_dir, 'install.sh')
    with open(script_path, 'w') as f:
        f.write(install_script)
    os.chmod(script_path, 0o755)
    # install applicationn and its dependencies using the script
    result = subprocess.run(['bash', script_path], capture_output=True, text=True)
    


def check_compatibility(app_code, version_id):
    """ Fetch app version compatibility and reconcile with this workspace legacy """
    api_comp = AlnodaApiApp('compatibility', app_code=app_code, version_id=version_id)
    res, app_compat = api_comp.fetch()
    if res is False: return False
    if 'all_workspaces' in app_compat: return True
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


def install_app(app_code, version=None, silent=False):
    """ Install app locally """
    # fetch app version
    if version is not None: 
        api = AlnodaApiApp('meta', app_code=app_code, version=version)
    else:
        api = AlnodaApiApp('meta',app_code=app_code)
    res, app_meta = api.fetch()
    if res is False:
        return False, "App or app version not found"
    version_id = app_meta['version_id']
    ### check compatibility
    if not silent: 
        is_compatible = check_compatibility(app_code, version_id)
        if not is_compatible:
            typer.echo("WARNING: This app is not explicitly compatible with any of the lineage workspace versions!")
            should_continue = typer.confirm("Do you want to continue?")
            if not should_continue: return
    ### Check if app exposes UI and wrkspace has free ports
    if 'app_port' in app_meta:
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
    ### Install app using the script
    install_app(app_meta)
    









    

        

