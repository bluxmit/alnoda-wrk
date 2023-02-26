import requests
import json

from .globals import ALNODA_API_DOMAIN, ALNODA_API_VERSION
ALNODA_API_DOMAIN = "https://api.alnoda.org"


class AlnodaApi:
    alnoa_api_url = f'{ALNODA_API_DOMAIN}/api/{ALNODA_API_VERSION}'
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

