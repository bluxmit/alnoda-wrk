'''
'''
import subprocess
import requests
import json

PYPI_URL_PATTERN = 'https://pypi.python.org/pypi/{package}/json'


def get_pipx_package_version(package_name):
    try:
        output = subprocess.check_output(['pipx', 'list']).decode('utf-8')
        lines = output.strip().split('\n')
        for line in lines:
            if package_name in line:
                parts = line.split(",")[0]
                version = parts.split(package_name)[-1]
                return version.strip()
    except: pass
    return None

def get_wrk_versions():
    """ Get current version of the wrk, and latest from pypi """
    # current version
    curret_version = get_pipx_package_version("alnoda-wrk")
    latest_version = None
    # try gettig latest version from pypi
    req = requests.get(PYPI_URL_PATTERN.format(package='alnoda_wrk'))
    if req.status_code == 200:
        try: j = json.loads(req.text.encode(req.encoding))
        except: j = json.loads(req.text)
        latest_version = j["info"]["version"]
    success = (curret_version is not None and latest_version is not None)
    return success, curret_version, latest_version


def update_wrk_to_latest():
    """ Update alnoda wrk to the latest version """
    try:
        output = subprocess.check_output(['pipx', 'upgrade', 'alnoda_wrk']).decode('utf-8')
        return True
    except: return False

