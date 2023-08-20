import os
import typer
from typing import Optional
import subprocess
from .builder import init_wrk, build_workspace, delete_wrk, install_mkdocs_deps
from .ui_builder import get_mkdocs_yml, update_mkdocs_yml
from .meta_about import *
from .wrk_supervisor import create_supervisord_file, stop_app
from .tui.admin import open_admin
from .install_app import add_app
from .zsh import add_user_env_var, add_user_alias
from .sign_in import add_token, delete_auth
from .cheatsheet import add_cheatsheet_section, add_cheatsheet_command, refresh_cheatsheet_page
from .links import add_links_section, add_links_url, refresh_links_page
from .fileops import read_meta
from .ports import make_port_forward_cmd, forward_port
from .upgrade import get_wrk_versions, update_wrk_to_latest
from .globals import get_bool_env_var
from .services import session_serve_static

app = typer.Typer()

def cls():
    """ Clean (terminal) screen """
    os.system('cls' if os.name == 'nt' else 'clear')
    return

@app.command()
def deps():
    """ Install/Update workspace UI dependencies """
    install_mkdocs_deps()
    return
    
@app.command()
def init():
    """ Initialize workspace UI folder """
    typer.echo("Initializing $HOME/.wrk")
    init_wrk()
    return

@app.command()
def refresh():
    """ Force refresh workspace UI"""
    refresh_from_meta()
    refresh_about()
    return

@app.command()
def delete():
    """ Delete workspace UI completely"""
    typer.echo("Deleting $HOME/.wrk")
    delete_wrk()
    return

@app.command()
def build(folder: str):
    """ Build workspace (use when building workspace Docker images) """
    typer.echo(f"Building the workspace from {folder} ...")
    build_workspace(folder)
    return

@app.command()
def id():
    """ Show workspace id """
    workspace_id = get_workspace_id()
    typer.echo(workspace_id)

@app.command()
def descr():
    """ Edit Workspace meta description interactively """
    edit_workspace_description()

@app.command()
def update(what, value):
    """ Update Workspace meta: name, version, author, description """
    if what == "name": update_workspace_name(value)
    elif what == "version": update_workspace_version(value)
    elif what == "author": update_workspace_author(value)
    elif what == "description": update_workspace_description(value)
    else: typer.echo(f"Cannot edit {what}")
    typer.echo("✅ Done!")
    return

@app.command()
def start(name: str, cmd: str):
    """
    Start application or service as daemon
    """
    create_supervisord_file(name, cmd)
    refresh_from_meta(); refresh_about()
    typer.echo("✅ Done!")
    typer.echo("❗ Service activation requires workspace reboot!")
    return

@app.command()
def stop(name: str):
    """
    Stop daemonnized application or service 
    """
    stop_app(name)
    refresh_from_meta(); refresh_about()
    typer.echo("✅ Done!")
    typer.echo("❗ Workspace reboot is required!")

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
def install(application, tab: Optional[str] = typer.Argument("home")):
    """
    Install app from Alnoda Hub
    """
    silent = get_bool_env_var("WRK_SILENT", default=False)
    if '==' in application:
        app_ = application.split('==')
        app_code = app_[0]
        version = app_[1] 
        add_app(app_code, version=version, page=tab, silent=silent)
    else:
        app_code = application 
        add_app(app_code, version=None, page=tab, silent=silent)
    return

@app.command()
def setvar(name, value):
    """
    Set terminal shell (zsh) environmental variable. Same as 'wrk env'
    """
    add_user_env_var(name, value)
    refresh_from_meta(); refresh_about()
    typer.echo("✅ Done!")
    typer.echo("❗ Terminal reload is required!")
    return

@app.command()
def env(name, value):
    """
    Set terminal shell (setvar) environmental variable. Same as 'wrk env'
    """
    add_user_env_var(name, value)
    refresh_from_meta(); refresh_about()
    typer.echo("✅ Done!")
    typer.echo("❗ Terminal reload is required!")
    return

@app.command()
def addpath(folder):
    """
    Add a folder to PATH, only applies to terminal zsh shell
    """
    varname = "PATH"
    varval = f'$PATH:{folder}'
    add_user_env_var(varname, varval)
    refresh_from_meta(); refresh_about()
    typer.echo("✅ Done!")
    typer.echo("❗ Terminal reload is required!")
    return

@app.command()
def alias(name, cmd):
    """
    Set alias for zsh terminal shell (name='value')
    """
    add_user_alias(name, cmd)
    typer.echo("✅ Done!")
    typer.echo("❗ Terminal reload is required!")

@app.command()
def signin(token):
    """
    Autheticate workspace at alnoda.org 
    """
    success, name = add_token(token)
    if success:  
        typer.echo(f"✨ Hello {name}!")
        return
    typer.echo(f"Could not authenticate")
    

@app.command()
def signout():
    """
    Log out workspace from alnoda.org 
    """
    delete_auth()
    typer.echo("👋 Goodbye!")

@app.command()
def cheatsec(name):
    """
    Add a section to the cheatsheet tab.  
    """
    add_cheatsheet_section(name)
    refresh_cheatsheet_page()
    typer.echo("✅ Done!")

@app.command()
def cheat(section, cmd, description):
    """
    Add cheatsheet command to some section
    """
    add_cheatsheet_command(section, cmd, description)
    refresh_cheatsheet_page()
    typer.echo("✅ Done!")

@app.command()
def linksec(name):
    """
    Add links section 
    """
    add_links_section(name)
    refresh_links_page()
    typer.echo("✅ Done!")

@app.command()
def link(section, url, name, description):
    """
    Add new link to the existing link section
    """
    add_links_url(section, url, name, description)
    refresh_links_page()
    typer.echo("✅ Done!")

@app.command()
def kill():
    """
    Restart workspace when running in k8s. Stops otherwise
    """
    typer.echo(f"⚠️ WARNING: this will stop the workspace.")
    should_continue = typer.confirm("Do you want to continue❓")
    if not should_continue: return
    else: os.system('cd /tmp; nohup sudo killall5 -9 &')


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
            should_continue = typer.confirm(f"New version available {latest_version}. Do you want to upgrade❓")
            if not should_continue: return
            update_wrk_to_latest()


@app.command()
def fw(from_port, to_port):
    """
    Froward traffic from [host:]from_port to to_port. Argument 'from_port' can be either port on localhost by default or address [host:port] 
    """
    forward_port(from_port, to_port)

@app.command()
def fwd(from_port, to_port):
    """
    Permanently forward traffic from [host:]from_port to to_port. Argument 'from_port' can be either port on localhost by default or address [host:port] 
    """
    success, cmd = make_port_forward_cmd(from_port, to_port)
    name = f"fwd{from_port}{to_port}"
    create_supervisord_file(name, cmd)
    typer.echo("🔀 Done!")
    typer.echo("❗ To start forwarding workspace reboot is required!")

@app.command()
def srv(port: int = typer.Argument(8026), folder: str = typer.Argument(None)):
    """
    Serve current directory with a static web server on [port]. Default is 8026 if port is not specified. 
    """
    session_serve_static(port, folder) 

@app.command()
def srvr(name, folder, port):
    """
    Start a permanent static web server in a specific folder on the defined workspace port. 
    """
    service_cmd = f'cd {folder} && python -m http.server {port}'
    create_supervisord_file(name, service_cmd)
    typer.echo("⚠️ Workspace restart is required! To restart execute 'wrk kill'")