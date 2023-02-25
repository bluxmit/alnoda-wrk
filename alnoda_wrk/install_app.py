""" Module to install applications from alnoda.org
"""
import os
import requests
import json
from .globals import WORKSPACE_DIR, ALNODA_API_URL


def fetch_app_details(app_code, version=None):
    """ Fetch app metadata """
    if version is None:
        url = f'{ALNODA_API_URL}/api/v1/app/{app_code}/meta/'
    else:
        url = f'{ALNODA_API_URL}/api/v1/app/{app_code}/{version}/meta/'
    response = requests.get(url)
    if response.status_code == 200:
        try:
            result = response.json()
            if 'error' in result:
                return False, result['error']
            else:
                return True, result
        except: pass
    return False, {}


def install_app(app_code, version=None):
    """ Install app locally """
    # fetch app version
    res, data = fetch_app_details(app_code, version)