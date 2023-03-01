import os
import requests
import json
from .globals import WORKSPACE_DIR, ALNODA_API_DOMAIN, ALNODA_API_VERSION

TOKEN_VERIFY_PATH = f"api/{ALNODA_API_VERSION}/token/verify/"
VERIFY_TOKEN_URL = f'{ALNODA_API_DOMAIN}/{TOKEN_VERIFY_PATH}'
AUTH_FILE = os.path.join(WORKSPACE_DIR, 'auth.json') 


def read_auth():
    """ ->> {}
    Reads existing auth data json file, and returns dict.

    :return: existing auth attributes as dict
    :rtype: dict
    """
    if not os.path.exists(AUTH_FILE):
        return {}
    with open(AUTH_FILE) as json_file:
        auth_dict = json.load(json_file)
    return auth_dict

def write_auth(token, username):
    """ {} ->> 
    Overwrite existing auth json with the updated token and username

    :param token: securitu tokent to authenticate workspace at alnoda.org
    :type token: str
    :param usernname: user name at alnoda.org
    :type token: str
    """
    with open(AUTH_FILE, 'w') as file:
        auth_dict = {'username': username, 'token': token}
        json.dump(auth_dict, file, indent=4 * ' ')
    return 

def add_token(token):
    """ Add verify security token, and save it (update auth file) if token is verified """
    # Data to send in the POST request
    data = {'token': token}
    response = requests.post(VERIFY_TOKEN_URL, data=data)
    if response.status_code == 200:
        try:
            result = response.json()
            if result['verified']:
                username = result['username']
                write_auth(token, username)
                return True
        except: pass
        return False

def verify_authenticated():
    """ Check if workspace is autheticated """
    auth = read_auth()
    if len(auth) == 0: return False
    try:
        username_ = auth['username']
        token_ = auth['token']
        data = {'token': token_}
        response = requests.post(VERIFY_TOKEN_URL, data=data)
        if response.status_code == 200:
            try:
                result = response.json()
                if result['verified']:
                    username = result['username']
                    if username_ == username:
                        return True
            except: pass
    except: pass
    return False

def delete_auth():
    """ Delete authentication dict """
    if os.path.exists(AUTH_FILE):
        os.remove(AUTH_FILE)
    return
