"""
Module with fuctions that aim to modify the running workspace
"""
import os 
import logging
from .globals import *
from .wrk_supervisor import create_supervisord_file


def start_app(name: str, cmd: str):
    """
    Start application
    """
    # start application 
    stream = os.popen(cmd+"&!")
    output = stream.read()
    output
    # Add to the supervisor (app will run even after workspace restart)
    cmd = f""" /bin/sh -c " {cmd} " """
    create_supervisord_file(name, cmd)