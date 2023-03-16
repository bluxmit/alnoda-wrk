import os
import typer
from .builder import init_wrk, build_workspace, delete_wrk, install_mkdocs_deps
from .ui_builder import get_mkdocs_yml, update_mkdocs_yml
from .meta_about import *
from .wrk_supervisor import create_supervisord_file
from .tui.admin import open_admin
from .install_app import add_app
from .zsh import add_user_env_var

app = typer.Typer()

def cls():
    """ Clean (terminal) screen """
    os.system('cls' if os.name == 'nt' else 'clear')
    return

@app.command()
def deps():
    """ Install/Update mkdocs dependencies """
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
    Start application
    """
    create_supervisord_file(name, cmd)
    return

@app.command()
def admin():
    """
    Open Admin TUI
    """
    open_admin()

@app.command()
def install(application):
    """
    Install app from alnoda.org
    """
    if '==' in application:
        app_ = application.split('==')
        app_code = app_[0]
        version = app_[1] 
        add_app(app_code, version=version, silent=False)
    else:
        app_code = application 
        add_app(app_code, version=None, silent=False)
    return

@app.command()
def setvar(name, value):
    """
    Set environmental variable name='value'
    """
    add_user_env_var(name, value)
    return
