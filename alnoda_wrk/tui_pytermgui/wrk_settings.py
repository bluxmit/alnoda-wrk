import pytermgui as ptg
import sys
import pyfiglet
from termcolor import colored
from myInputField import myInputField
import time


CONFIG = """
config:
    InputField:
        styles:
            prompt: dim italic
            cursor: '@72'

    Label:
        styles:
            value: dim bold

    Window:
        styles:
            border: '60'
            corner: '60'
        overflow: scroll

    Container:
        styles:
            border: '96'
            corner: '96'
        overflow: scroll

    Button:
        styles:
            label: '[@39 255 bold]{item}'
            highlight: '[@222 24 bold]{item}'
            cursor: '@72'
    
    Splitter:
        chars:
            separator: "  "
"""

with ptg.YamlLoader() as loader:
    loader.load(CONFIG)




def get_main_settings_window():
    window = (
        ptg.Window(
            "",
            ptg.Label(colored(pyfiglet.figlet_format("Alnoda", font="banner3-D"), 'red')),
            "", "", 
            ptg.Button("Features", onclick=lambda *_: features_btn(manager, window)),
            "", 
            ptg.Button("Description", onclick=lambda *_: description_btn(manager, window)),
            "",
            ptg.Button("Quit", onclick=lambda *_: sys.exit()),
            width=120,
            height=20,
            box="DOUBLE",
            is_static=True,
        )
        .set_title("[210 bold]Settings")
        .center()
    )
    return window



def save_features(manager, window):
    manager.remove(window)
    main_window = get_main_settings_window()
    manager.add(main_window)


def cancel_features_edit(manager, window):
    manager.remove(window)
    main_window = get_main_settings_window()
    manager.add(main_window)

def get_features_window():
    features_window = ptg.Window(
        "",
        ptg.InputField("Workspace name", prompt="Workspace name: "),
        ptg.InputField("Workspace version", prompt="Workspace version: "),
        ptg.InputField("Workspace author", prompt="Workspace author: "),
        "", "",
        ptg.Splitter(
                    ["Cancel", lambda *_: save_features(manager, features_window)],
                    ["Save", lambda *_: cancel_features_edit(manager, features_window)]
                ),
        width=80,
        height=5,
        box="DOUBLE",
        is_static=True,
        is_modal = True
    ).set_title("[220 bold]Edit workspace features").center()
    return features_window

def features_btn(manager, window):
    manager.remove(window)
    features_window = get_features_window()
    features_window.focus()
    manager.add(features_window)
    return





def save_description(manager, description_window):
    manager.remove(description_window)
    main_window = get_main_settings_window()
    manager.add(main_window)

def cancel_description_edit(manager, description_window):
    manager.remove(description_window)
    main_window = get_main_settings_window()
    manager.add(main_window)

def get_description_window():
    description_window = ptg.Window(
        "",
        myInputField(
            "A whole bunch ofMeaningful notesand stuff", multiline=True
        ),
        "", "",
        ptg.Splitter(
            ptg.Button("Cancel", lambda *_: save_description(manager, description_window)),
            ptg.Button("Save", lambda *_: cancel_description_edit(manager, description_window))
                ),
        width=100,
        height=10,
        box="DOUBLE",
        is_static=True,
        is_modal = True
    ).set_title("[220 bold]Edit workspace description").center()
    return description_window

def description_btn(manager, window):
    manager.remove(window)
    description_window = get_description_window()
    description_window.focus()
    manager.add(description_window)
    return



with ptg.WindowManager() as manager:
    main_window = get_main_settings_window()
    manager.add(main_window)