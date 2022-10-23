from pathlib import Path
from jinja2 import Template
import threading
import time
import subprocess

from .templates import frpc_http_template
from .globals import *

FRP_FOLDER = os.path.join(HOME_DIR, '.frp')
FRP_REQUIRED_SUFFIX = "web"
FRPC_INI_FILE = os.path.join(FRP_FOLDER, 'frpc.ini')
FRPC_BINARY = "/home/abc/apps/frp/frpc"
FRP_SERVER = "opensource-platform.com"
# token is temporarily static, later will be requested from server
FRP_TOKEN = "d326ffbd243ee8ceb85d29169e4b92e7"
FRP_BANDWIDTH_LIMIT = "500KB"


def init_frp_dir():
    """ Make sure FRP folder exists
    """
    Path(FRP_FOLDER).mkdir(parents=True, exist_ok=True)
    return

def write_frpc_ini(port):
    """ Generates and writes frpc.ini file to expose application running 
    on some port. It uses templates and creates random subdomain.

    :param name: workspace name
    :type name: str
    :return: URL over which anyone can access your service
    :rtype: str
    """
    frp_data = {}
    frp_data["local_port"] = str(port)
    frp_data["server_url"] = FRP_SERVER
    frp_data["token"] = FRP_TOKEN
    frp_data["bandwidth_limit"] = FRP_BANDWIDTH_LIMIT
    code = get_code(10)
    subdomain = f"{code}{FRP_REQUIRED_SUFFIX}"
    frp_data["subdomain"] = subdomain
    tm = Template(frpc_http_template)
    frpc_ini = tm.render(data=frp_data)
    # save frpc.ini file 
    with open(FRPC_INI_FILE, "w") as f:
        # owerwrite frpc file
        f.write(frpc_ini)
    return subdomain

def run_frpc_process():
    while true:
        print(".")
        time.sleep(1)

def expose_port(port):
    """
    """
    # first make sure frp folder initialized
    init_frp_dir()
    # write frpc.ini file 
    subdomain = write_frpc_ini(port)
    # create thread where launch frpc system process
    timelimit = 2 * 60 
    cmd = f"timelimit -t{timelimit} {FRPC_BINARY} -c {FRPC_INI_FILE}"
    # create thread that kills frpc thread after session expires
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    time.sleep(2)
    poll = process.poll()
    if poll is not None: 
        return False
    # return subdomain
    full_url = f'https://{subdomain}.{FRP_SERVER}/'
    return full_url
    