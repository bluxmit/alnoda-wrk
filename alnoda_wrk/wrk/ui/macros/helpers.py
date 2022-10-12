"""
Basic example of a Mkdocs-macros module.
Include this  {{ macros_info() }} in any page to get complete macro info
"""
import os
import json


def get_apps_dict():
    """ -> {}
    Read json with app UI dataforallpages
    :return: applications configuration dict
    :rtype: dict
    """
    with open('conf/ui-apps.json') as json_file:
        apps_dict = json.load(json_file)
    return apps_dict


def get_workspace_home_port():
    """ -> int
    Define the port for the Workspace Home page
    :return: port for the workspace Home page
    :rtype: int
    """
    workspace_home_port = 8020
    try:
        workspace_home_port = int(os.environ["WRK_HOME_PORT"])
    except:
        pass
    return workspace_home_port


def add_path(url, v):
    """ str, {} -> str
    If path is defined, add it to the URL
    """
    if "path" in v and len(str(v['path'])) > 0:
        if v["path"][0] == "/": path = v["path"][1:] 
        else: path = v["path"]
        url = f"{url}/{path}"
    return url


def get_url(app, v, workspace_home_port):
    """ Get URL for every app. 
    Workspace can run on different ports or hosts.

    This function tries different approaches:
        1. If there is an env var with the app key + '_URL' it will take it entirely.
            This is the way to everride any URL
        2. If there is env var 'WRK_DOMAIN' - it will prepend port to the domain, i.e. p-<port>-<WRK_DOMAIN>
            If there is in addition env. var 'WRK_DOMAIN_PREFIX' it will construct <WRK_DOMAIN_PREFIX>-<port>-<WRK_DOMAIN>
            If domain is defined, the URL will always have protocol https
        3. Construct URL piece-by-piece 
    """
    app = app.upper()
    
    #### Try to get the entire URL from the env variable
    try:
        url = os.environ[f"{app}_URL"]
        return add_path(url, v)
    
    #### Use env. vars WRK_DOMAIN & WRK_DOMAIN_PREFIX
    except:
        domain_prefix = 'p'
        try: domain_prefix = os.environ["WRK_DOMAIN_PREFIX"]
        except: pass
        try:
            wrk_domain = os.environ["WRK_DOMAIN"]
            url = f"https://{domain_prefix}-{v['port']}.{wrk_domain}"
            return add_path(url, v)
        
        #### Construct URL piece-by-piece
        except:
            ## Host
            host = "localhost" # <- default host
            # Try to get host environment from the env variable
            try: host = os.environ["WRK_HOST"]
            except: pass

            ## Protocol
            proto = "http" # <- default protocol
            # Try to get protocol from environment from the env variable
            try: proto = os.environ["WRK_PROTO"] # <- i.e. https when self-hosted on cloud server
            except: pass

            ## Port increment 
            # if other ports should be exposed
            port_increment = int(v['port']) - 8020
            port = workspace_home_port + port_increment

            ## Construct URL
            url = f"{proto}://{host}:{port}"
            return add_path(url, v)


# this function name should not be changed
def define_env(env):
    """
    This is the hook for defining variables, macros and filters
    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    - filter: a function with one of more arguments,
        used to perform a transformation
    """
    @env.macro
    def get_page_apps(page):
        # get UI port (from environmental variable)
        workspace_home_port = get_workspace_home_port()
        # read page dict
        apps_dict = get_apps_dict()
        page_dict_raw = apps_dict[page]
        # enrich page dict with URLs
        page_dict = []
        for p,v in page_dict_raw.items():
            v['app_url'] = get_url(p, v, workspace_home_port)
            page_dict.append(v)
        return page_dict


            