import requests
from .globals import WORKSPACE_DIR, ALNODA_API_URL

TOKEN_VERIFY_PATH = f"api/v1/token/verify/"
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
    return Oauth_dict

def write_auth(token, username):
    """ {} ->> 
    Overwrite existing auth json with the updated token and username

    :param token: securitu tokent to authenticate workspace at alnoda.org
    :type token: str
    :param usernname: user name at alnoda.org
    :type token: str
    """
    with open(LINKS_DATA_FILE, 'w') as file:
        json.dump(links_dict, file, indent=4 * ' ')
    return 

def add_token(token):
    """ Add verify security token, and save it (update auth file) if token is verified """
    url = f'{ALNODA_API_URL}/{TOKEN_VERIFY_PATH}'
    # Data to send in the POST request
    data = {'token': token}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        try:
            result = response.json()
            if result['verified']:
                username = result['username']
                # save token, username
                
        except: pass



