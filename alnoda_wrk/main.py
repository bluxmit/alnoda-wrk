import os
import typer
import inquirer
from rich.prompt import Prompt
import TermTk as ttk
from .builder import init_wrk, build_workspace, delete_wrk, install_mkdocs_deps
from .ui_builder import get_mkdocs_yml, update_mkdocs_yml
from .meta_about import *
from .wrk_modifiers import start_app
from .tui.admin import AlnodaAdminTUI

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
    return

@app.command()
def edit():
    """ Update Workspace meta """
    questions = [
        inquirer.List('name',
                    message="What do you want to edit?",
                    choices=['name', 'version', 'author', 'description'],
        ),
    ]
    what = inquirer.prompt(questions)['name']
    cls()
    if what == "name":
        value = Prompt.ask("Enter new workspace name :robot:")
        update_workspace_name(value)
        # update mkdocs.yml too
        mkyml = get_mkdocs_yml()
        mkyml["site_name"] = value
        update_mkdocs_yml(mkyml)
    elif what == "version":
        value = Prompt.ask("Enter new workspace version :stopwatch:")
        update_workspace_version(value)
    elif what == "author":
        value = Prompt.ask("Enter new workspace author :sunglasses:")
        update_workspace_author(value)
    elif what == "description":
        edit_workspace_description()
    else:
        typer.echo(f"Cannot edit {what}")
    typer.echo(f"Done! :okay:")
    return

@app.command()
def run(name: str, cmd: str):
    """
    Start application
    """
    start_app(name, cmd)
    return


@app.command()
def admin():
    """
    Open Admin TUI
    """
    root = ttk.TTk()
    root.setLayout(ttk.TTkGridLayout())
    AlnodaAdminTUI(root)
    root.mainloop()