import os
from pathlib import Path

HOME_DIR = Path.home()
WORKSPACE_DIR = os.path.join(HOME_DIR, '.wrk') 
WORKSPACE_UI_DIR = os.path.join(WORKSPACE_DIR, 'ui')
WORKSPACE_META_FILE = os.path.join(WORKSPACE_DIR, 'meta.json')
WORKSPACE_LINEAGE_FILE = os.path.join(WORKSPACE_DIR, 'lineage.json')
WORKSPACE_UI_SCSS_STYLES_FILE = os.path.join(WORKSPACE_UI_DIR, 'docs', 'stylesheets', 'extra.css')
SUPERVISORD_FOLDER = "/etc/supervisord"
VAR_LOG_FOLDER = "/var/log/workspace/"
WORKSPACE_HOME_PAGES = ["home", "admin", "my_apps"]
WORKSPACE_PAGES_ODER = {"Home": 1, "My apps": 2, "Admin": 3, "About": 9, "Docs": 10}
# external os text editor for interactive inputs
TEXT_EDITOR = "mcedit"


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