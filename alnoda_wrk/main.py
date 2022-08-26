import typer
from .builder import init_wrk, build_workspace, delete_wrk, install_mkdocs_deps
from .ui_builder import get_mkdocs_yml, update_mkdocs_yml
from .meta_about import *
from .wrk_modifiers import start_app

app = typer.Typer()


@app.command()
def deps():
    """ 
    Install/Update mkdocs dependencies
    """
    install_mkdocs_deps()
    return
    

@app.command()
def init():
    """
    Initialize workspace folder
    """
    typer.echo("Initializing $HOME/.wrk")
    init_wrk()
    return


@app.command()
def delete():
    """
    Delete local .wrk folder
    """
    typer.echo("Deleting $HOME/.wrk")
    delete_wrk()
    return


@app.command()
def build(folder: str):
    """
    Build workspace
    """
    typer.echo(f"Building the workspace from {folder} ...")
    build_workspace(folder)
    return


@app.command()
def edit(what: str = "description"):
    """
    Edit Workspace meta (description by default) interactively
    """
    if what == "description":
        edit_workspace_description()
    else:
        typer.echo(f"Cannot edit {what}")
    return


@app.command()
def update(what, value):
    """
    Update Workspace meta 
    """
    if what == "name":
        update_workspace_name(value)
        # update mkdocs.yml too
        mkyml = get_mkdocs_yml()
        mkyml["site_name"] = value
        update_mkdocs_yml(mkyml)
    elif what == "version":
        update_workspace_version(value)
    elif what == "author":
        update_workspace_author(value)
    elif what == "description":
        update_workspace_description(value)
    else:
        typer.echo(f"Cannot edit {what}")
    return


@app.command()
def refresh(what: str = "about"):
    """
    Force refresh some of the workspace parts
    """
    if what == "about":
        refresh_about()


@app.command()
def start(name: str, cmd: str):
    """
    Start application
    """
    start_app(name, cmd)