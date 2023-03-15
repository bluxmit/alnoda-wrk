from pathlib import Path
from jinja2 import Template
import threading
import time
import subprocess
import random
import socket

from .templates import frpc_http_template
from .globals import *
from .sign_in import verify_authenticated

FRP_FOLDER = os.path.join(HOME_DIR, '.frp')
FRPC_INI_FILE = os.path.join(FRP_FOLDER, 'frpc.ini')
FRPC_BINARY = "/home/abc/apps/frp/frpc"
FRP_SERVERS = {
    'fkpakr': {'port': 7000},
    'dcjdhx': {'port': 7001},
    'cmndbq': {'port': 7002},
    'kvopp': {'port': 7003},
    'fowopd': {'port': 7004}
}
FRP_SERVER = "alnoda.net"
# token is temporarily static, later will be requested from server
FRP_TOKEN = "d326ffbd243ee8ceb85d29169e4b92e7"
# Can be configured in future
FRP_BANDWIDTH_LIMIT = "500KB"
MAX_FRP_PROCESSES = 1
SESSION_DURATION_MIN = 20
# For authenticated users
AUTHENTICATED_FRP_BANDWIDTH_LIMIT = "1MB"
AUTHENTICATED_MAX_FRP_PROCESSES = 1
AUTHENTICATED_SESSION_DURATION_MIN = 40


def init_frp_dir():
    """ Make sure FRP folder exists
    """
    Path(FRP_FOLDER).mkdir(parents=True, exist_ok=True)
    return

def choose_frp_server():
    """ Chooses one of the frp servers

    :return: server port (7000-7004)
    :rtype: int
    :return: server suffixes
    :rtype: str
    """
    server_suffixes = list(FRP_SERVERS.keys())
    suffix = random.choice(server_suffixes)
    port = FRP_SERVERS[suffix]['port']
    return port, suffix

def write_frpc_ini(port, server_port, suffix, frp_bandwidth_limit):
    """ Generates and writes frpc.ini file to expose application running 
    on some port. It uses templates and creates random subdomain.

    :param port: workspace application internal port to expose over the Internet
    :type port: int
    :param server_port: frp server port to use
    :type port: int
    :param suffix: frp server suffix to use
    :type port: str
    :return: URL over which anyone can access your service
    :rtype: str
    """
    # now create frpc file
    frp_data = {}
    frp_data["local_port"] = str(port)
    frp_data["server_port"] = str(server_port)
    frp_data["server_url"] = FRP_SERVER
    frp_data["token"] = FRP_TOKEN
    frp_data["bandwidth_limit"] = frp_bandwidth_limit
    code = get_code(10)
    subdomain = f"{code}{suffix}"
    frp_data["subdomain"] = subdomain
    tm = Template(frpc_http_template)
    frpc_ini = tm.render(data=frp_data)
    # save frpc.ini file 
    with open(FRPC_INI_FILE, "w") as f:
        # owerwrite frpc file
        f.write(frpc_ini)
    return subdomain


def can_connect_frp_server(server_port):
    """ Check if respective FRP server port is open and accessible

    :param server_port: frp server port
    :type server_port: int
    :return: whether frp server port is pen and accessible
    :rtype: bool
    """
    can_connect = False
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(7)
        result = sock.connect_ex((FRP_SERVER, server_port))
        if result == 0: 
            can_connect = True
        sock.close()
    except:
        can_connect = False
    return can_connect


def expose_port(port):
    """ Exposes application WEB UI running on a specific port

    :param port: workspace application port
    :type port: int
    :return: whether calling sharing service was successful
    :rtype: bool
    :return: error message or extra data
    :rtype: str/dict
    """
    # get server port and suffix
    server_port, suffix = choose_frp_server()
    # check connectivity 
    if not can_connect_frp_server(server_port):
        return False, f'Cannot connect to the server. No Internet connection? Firewall blocking?'
    # get defaul values for session 
    session_duration_min = SESSION_DURATION_MIN
    max_num_frp_processes = MAX_FRP_PROCESSES
    frp_bandwidth_limit = FRP_BANDWIDTH_LIMIT
    # improve limits for authenticated users
    if verify_authenticated():
        session_duration_min = AUTHENTICATED_SESSION_DURATION_MIN
        max_num_frp_processes = AUTHENTICATED_MAX_FRP_PROCESSES 
        frp_bandwidth_limit = AUTHENTICATED_FRP_BANDWIDTH_LIMIT 
    # create command for frp process
    timelimit = session_duration_min * 60
    frpcmd = f"{FRPC_BINARY} -c {FRPC_INI_FILE}"
    cmd = f"timelimit -t{timelimit} {frpcmd}"
    # make sure frp folder initialized
    init_frp_dir()
    # check nnumber of parallel processes is nnot exceeding the limit
    scm = f'ps axf | grep "\\_ {frpcmd}" | grep -v "grep"'
    try:
        res = subprocess.check_output(scm, shell=True, text=True)
        procs = res.split("\n")
        if len(procs) > max_num_frp_processes:
            return False, f'You cannot share more than {max_num_frp_processes} application(s) at a time.'
    except: pass
    # write frpc.ini file 
    subdomain = write_frpc_ini(port, server_port, suffix, frp_bandwidth_limit)
    # create thread that kills frpc thread after session expires
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    time.sleep(2)
    poll = process.poll()
    if poll is not None: 
        return False, "Please try again"
    # return true as success and extra data
    full_url = f'https://{subdomain}.{FRP_SERVER}/'
    extra = {'full_url': full_url, 'session_duration_min': session_duration_min, 'bandwidth_limit': frp_bandwidth_limit, 'max_num_frp_processes': max_num_frp_processes}
    return True, extra
    