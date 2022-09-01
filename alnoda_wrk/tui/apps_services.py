import copy
import TermTk as ttk
from ..wrk_supervisor import get_started_apps
from .gvars import *

CREATE_NEW = "START NEW"


def get_apps_services_widget():
    # Get existing apps and services
    apps = get_started_apps()
    new_apps = copy.deepcopy(apps)
    apps_list = list(apps.keys())
    apps_list.append(CREATE_NEW)
    extra = {'choice': ""}

    # Generate widgets
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)
    scrollArea = ttk.TTkScrollArea(parent=None, border=0, minHeight=25)
    wrap_widg.layout().addWidget(scrollArea)
    l = 2; ls = 20
    r = 25; rs = 90 
    row = 1 

    ttk.TTkLabel(text='App / Service', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    app_select = ttk.TTkComboBox(list=apps_list, pos=(r,row), size=(rs,1))
    scrollArea.viewport().addWidget(app_select)

    row+=2; ttk.TTkLabel(text='Command', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    cmd_inp = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1))
    scrollArea.viewport().addWidget(cmd_inp)

    row+=2; name_lab = ttk.TTkLabel(text='Name', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=False)
    name_inp = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1), visible=False)
    scrollArea.viewport().addWidget(name_inp)

    # Buttons
    row+=2; remove_btn = ttk.TTkButton(text='Remove', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=False)
    remove_btn.setBorderColor(TTkColor.fg('#f20e0a'))
    row+=17; btn_cancel = ttk.TTkButton(text='Cancel', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=False)
    btn_save = ttk.TTkButton(text='Save', pos=(r,row), size=(rs,1), parent=scrollArea.viewport(), visible=False)

    def appSelectHandler(i):
        choice = apps_list[i]
        extra['choice'] = choice
        if choice != CREATE_NEW:
            cmd = apps[choice]
            cmd_inp._text = cmd; cmd_inp.update()
            # Show delete, cancel and save buttons
            remove_btn.show()
            btn_cancel._visible=True; btn_cancel.update()
            btn_save._visible=True; btn_save.update()
            name_lab.hide(); name_inp.hide()
        else:
            remove_btn.hide()
            btn_cancel._visible=True; btn_cancel.update()
            btn_save._visible=True; btn_save.update()
            name_lab._visible=True; name_lab.update()
            name_inp._visible=True; name_inp.update()
            name_lab.show(); name_inp.show()
            cmd_inp._text = ""; cmd_inp.update()
    app_select.currentIndexChanged.connect(lambda i : appSelectHandler(i))

    # Text input processor (CMD)
    def _processCMDInput(n): 
        pass
    # Bind Text input processor (Font)
    cmd_inp.textEdited.connect(lambda n: _processCMDInput(n))

    return wrap_widg