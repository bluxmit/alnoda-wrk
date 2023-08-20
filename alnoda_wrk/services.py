import subprocess
import atexit
import typer
import time
from .globals import * 

def session_serve_static(port):
    """ Serve static website in a current session """
    if int(port) not in WRK_MYAPPS_PORTS:
        err = f'Port must be one of the "My apps" ports: {", ".join([str(i) for i in WRK_MYAPPS_PORTS])}'
        typer.echo(f"❗ {err}")
        return
    srv_cmd = f'python -m http.server {port}'
    process = subprocess.Popen(srv_cmd, shell=True, stdout=subprocess.PIPE)
    poll = process.poll()
    if poll is not None: 
        err = f'Failed to start static server on port {port}.'
        typer.echo(f"❗ {err}")
        return
    else:
        typer.echo(f"✔️ Serving current folder on port {port}. 'Ctrl + c' to stop")
        while True: 
            time.sleep(1)

