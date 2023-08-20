import os
from pathlib import Path
import random, string

HOME_DIR = Path.home()
WORKSPACE_DIR = os.path.join(HOME_DIR, '.wrk') 
WORKSPACE_UI_DIR = os.path.join(WORKSPACE_DIR, 'ui')
WORKSPACE_META_FILE = os.path.join(WORKSPACE_DIR, 'meta.json')
WORKSPACE_LINEAGE_FILE = os.path.join(WORKSPACE_DIR, 'lineage.json')
WORKSPACE_UI_SCSS_STYLES_FILE = os.path.join(WORKSPACE_UI_DIR, 'docs', 'stylesheets', 'extra.css')
SUPERVISORD_FOLDER = "/etc/supervisord"
VAR_LOG_FOLDER = "/var/log/workspace/"
WORKSPACE_HOME_PAGES = ["home", "admin", "my_apps"]
WORKSPACE_PAGES_ODER = {"Home": 1, "My apps": 2, "Admin": 3, "About": 7, "Cheatsheet": 8, "Docs": 10}
# external os text editor for interactive inputs
TEXT_EDITOR = "mcedit"
ALNODA_API_DOMAIN = "https://api.alnoda.org"
ALNODA_API_VERSION = 'v1'
ALLOWED_FREE_PORT_RANGE_MIN = 8029
ALLOWED_FREE_PORT_RANGE_MAX = 8040
WRK_RESERVED_PORTS = [8022, 8023, 8024, 8025]
WRK_MYAPPS_PORTS = [8026, 8027, 8028]
AUTO_PORT_FWD_PREFIX = 'xig6c'
SYSTEM_APP_PREFIX = 'ficv7'


def safestring(s, length=15):
    """ str, int ->> str 
    Creates a 'safe' string - no spaces, special characters, all lowercase. 
    Such a string can be used for example in supervisord app name, env var, as variable, etc.

    :param name: string to make 'safe'
    :type name: str
    :param length: max length of the string
    :type length: int
    :return: safe string - no spaces, special characters, all lowercase
    :rtype: str
    """
    # use isalnum
    s = ''.join(e for e in s if e.isalnum())
    # make all lowercase
    s = s.lower()
    # make sure string has max length 
    s = s[:length]
    return s

def get_code(length=8):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return(result_str.lower())

def pref_url(url):
    # make url ok 
    correct = False
    if not url.startswith("https://") or url.startswith("http://"):
        url = "//"+url 
    return url

def clnstr(s):
    """Replace some chars from string input """
    s_ = s.replace('\r','').replace('\t','').replace('\b','').replace('\f','').replace('\ooo','')
    return s_

def get_bool_env_var(var_name, default=False):
    true_values = {"yes", "y", "true", "True", "t", "1"}
    false_values = {"no", "n", "false",  "False", "f", "0"}
    value = os.environ.get(var_name, "").lower()
    if value in true_values:
        return True
    elif value in false_values:
        return False
    else:
        return default

def kill_process(p):
    """ If you need to start system process that will be killed when python process terminates 
    Example:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        atexit.register(kill_process, process) 
    """
    try:
        p.kill()  # This sends a SIGKILL, which cannot be caught or ignored
    except ProcessLookupError:
        pass  # Process might have already terminated