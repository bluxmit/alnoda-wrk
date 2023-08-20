import subprocess
import atexit
import typer
import time
from .globals import * 


def session_serve_static(port, folder):
    """ Serve static website in a current session """
    if folder is None:
        srv_cmd = f'python -m http.server {port}'
        folder_str = "current folder"
    else:
        srv_cmd = f'cd {folder} && python -m http.server {port}'
        folder_str = f'folder {folder}'
    process = subprocess.Popen(srv_cmd, shell=True, stdout=subprocess.PIPE)
    poll = process.poll()
    if poll is not None: 
        err = f'Failed to start static server on port {port}.'
        typer.echo(f"❗ {err}")
        return
    else:
        typer.echo(f"✔️ Serving {folder_str} on port {port}. 'Ctrl + c' to stop")
        while True: 
            time.sleep(1)
            