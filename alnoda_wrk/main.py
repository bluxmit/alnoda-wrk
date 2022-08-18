import typer
from .builder import init_wrk, build_workspace
from .meta_about import *

app = typer.Typer()


@app.command()
def init():
    """
    Initialize workspace folder
    """
    typer.echo("Initializing $HOME/.wrk")
    init_wrk()
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
    elif what == "version":
        update_workspace_version(value)
    elif what == "author":
        update_workspace_author(value)
    elif what == "description":
        update_workspace_description(value)
    else:
        typer.echo(f"Cannot edit {what}")
    return
