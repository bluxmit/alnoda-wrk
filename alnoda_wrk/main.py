import os
from typing import Optional
import typer
import subprocess
from .builder import init_wrk, build_workspace, delete_wrk, install_mkdocs_deps
from .ui_builder import get_mkdocs_yml, update_mkdocs_yml
from .meta_about import *
from .wrk_supervisor import create_supervisord_file, stop_app
from .tui.admin import open_admin
from .install_app import add_app
from .zsh import add_user_env_var, add_user_alias
from .sign_in import add_token, delete_auth
from .cheatsheet import add_cheatsheet_section, add_cheatsheet_command
from .links import add_links_section, add_links_url
from .fileops import read_meta
from .upgrade import get_wrk_versions, update_wrk_to_latest

app = typer.Typer()

def cls():
    """ Clean (terminal) screen """
    os.system('cls' if os.name == 'nt' else 'clear')
    return

@app.command()
def deps():
    """ Install/Update wrk dependencies """
    install_mkdocs_deps()
    return
    
@app.command()
def init():
    """ Initialize workspace folder """
    typer.echo("Initializing $HOME/.wrk")
    init_wrk()
    return

@app.command()
def delete():
    """ Delete local .wrk folder """
    typer.echo("Deleting $HOME/.wrk")
    delete_wrk()
    return

@app.command()
def build(folder: str):
    """ Build workspace (use in docker build) """
    typer.echo(f"Building the workspace from {folder} ...")
    build_workspace(folder)
    return

@app.command()
def id():
    """ Show workspace id """
    workspace_id = get_workspace_id()
    typer.echo(workspace_id)

@app.command()
def edit(what: str = "description"):
    """ Edit Workspace meta (description by default) interactively """
    if what == "description":
        edit_workspace_description()
    else:
        typer.echo(f"Cannot edit {what}")
    return

@app.command()
def update(what, value):
    """ Update Workspace meta (non-interactive) """
    if what == "name": update_workspace_name(value)
    elif what == "version": update_workspace_version(value)
    elif what == "author": update_workspace_author(value)
    elif what == "description": update_workspace_description(value)
    else: typer.echo(f"Cannot edit {what}")
    return

@app.command()
def refresh():
    """ Force refresh workspace from meta"""
    refresh_from_meta()
    refresh_about()
    return

@app.command()
def start(name: str, cmd: str):
    """
    Start application or service as daemon
    """
    create_supervisord_file(name, cmd)
    return

@app.command()
def stop(name: str):
    """
    Stop daemonnized application or service 
    """
    stop_app(name)

@app.command()
def admin():
    """
    Open Admin TUI
    """
    open_admin()

@app.command()
def apps():
    """ Display list of apps installed from alnoda.org
    """
    meta_dict = read_meta()
    if "alnoda.org.apps" not in meta_dict  or len(meta_dict["alnoda.org.apps"]) == 0:
        typer.echo(f"you don't have any apps installed!")
        return
    else:
        for k,v in meta_dict["alnoda.org.apps"].items():
            try:
                typer.echo(f"❇️ {k}")
                typer.echo(f"Name:        {v['name']}")
                typer.echo(f"Version:     {v['version']}")
                typer.echo(f"Description: {v['description']}")
            except: pass

@app.command()
def install(application, page: Optional[str] = typer.Argument("home"), silent: Optional[bool] = typer.Argument(False)):
    """
    Install app from alnoda.org
    """
    if '==' in application:
        app_ = application.split('==')
        app_code = app_[0]
        version = app_[1] 
        add_app(app_code, version=version, page=page, silent=silent)
    else:
        app_code = application 
        add_app(app_code, version=None, page=page, silent=silent)
    return

@app.command()
def setvar(name, value):
    """
    Set zsh environmental variable name value. Same as 'wrk env'
    """
    add_user_env_var(name, value)
    return

@app.command()
def env(name, value):
    """
    Set zsh environmental variable name value. Same as 'wrk setvar'
    """
    add_user_env_var(name, value)
    return

@app.command()
def addpath(folder):
    """
    Add folder to PATH. Only applies to zsh
    """
    varname = "PATH"
    varval = f'$PATH:{folder}'
    add_user_env_var(varname, varval)
    return

@app.command()
def alias(name, cmd):
    """
    Set alias for zsh name='value'
    """
    add_user_alias(name, cmd)

@app.command()
def signin(token):
    """
    Autheticate workspace at alnoda.org 
    """
    add_token(token)

@app.command()
def signout():
    """
    Log out workspace from alnoda.org 
    """
    delete_auth()

@app.command()
def cheatsec(name):
    """
    Add cheatsheet section 
    """
    add_cheatsheet_section(name)

@app.command()
def cheat(section, cmd, description):
    """
    Add cheatsheet command to some section
    """
    add_cheatsheet_command(section, cmd, description)

@app.command()
def linksec(name):
    """
    Add links section 
    """
    add_links_section(name)

@app.command()
def link(section, url, name, description):
    """
    Add new record to the existing link section  
    """
    add_links_url(section, url, name, description)

@app.command()
def kill():
    """
    Restart workspace when running in k8s. Stops otherwise
    """
    typer.echo(f"⚠️ WARNING: this will stop the workspace.")
    should_continue = typer.confirm("Do you want to continue❓")
    if not should_continue: return
    else: subprocess.Popen("/sbin/killall5", shell=True, stdout=subprocess.PIPE)


@app.command()
def upgrade():
    """
    Upgrade wrk version
    """
    success, curret_version, latest_version = get_wrk_versions()
    if not success:
        typer.echo(f"Could not get alnoda_wrk versions. No Internet connection?")
    else:
        if curret_version == latest_version:
            typer.echo(f"✔️ Already latest version {curret_version}")
        else:
            typer.echo(f"Current version {curret_version}")
            should_continue = typer.confirm("New version available {latest_version}. Do you want to upgrade❓")
            if not should_continue: return
            update_wrk_to_latest()
