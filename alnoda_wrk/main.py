import typer
from .builder import init_wrk, build_workspace

app = typer.Typer()


@app.command()
def init():
    """
    Initialize workspace folder
    """
    typer.echo("Initializing $HOME/.wrk")
    init_wrk()


@app.command()
def build():
    """
    Build workspace
    """
    typer.echo("Building the workspace")

