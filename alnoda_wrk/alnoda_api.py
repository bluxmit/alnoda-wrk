import requests
import json

from .globals import ALNODA_API_DOMAIN, ALNODA_API_VERSION
from .sign_in import read_auth
from .fileops import read_meta


class AlnodaApi:
    def __init__(self, path):
        self.url = f'{ALNODA_API_DOMAIN}/api/v1/{path}'
    def fetch(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                try:
                    result = response.json()
                    if 'error' in result:
                        return False, result['error']
                    elif len(result) == 0:
                        return False, {}
                    else:
                        return True, result
                except: pass
        except: pass
        return False, {}


class AlnodaSignedApi:
    def __init__(self, path):
        self.url = f'{ALNODA_API_DOMAIN}/api/v1/{path}'
        self.authenticated = False
        try:
            auth_dict = read_auth()
            security_token = auth_dict['token']
            meta = read_meta()
            self.payload = {
                'token': security_token, 
                'workspace_id': meta['workspace_id'], 
                'workspace_name': meta['name'],
                'workspace_version': meta['version'],
                'workspace_created': meta['created']
                }
            self.authenticated = True
        except: pass

    def fetch(self, data):
        if not self.authenticated:
            return False, {'error': 'Not authenticated at alnoda.org'} 
        self.payload.update(data)
        try:
            headers = {'Content-type': 'application/json'}
            response = requests.post(self.url, json=self.payload, headers=headers)
            if response.status_code == 200:
                try:
                    result = response.json()
                    if 'error' in result:
                        return False, result['error']
                    elif len(result) == 0:
                        return False, {}
                    else:
                        return True, result
                except: pass
        except: pass
        return False, {}