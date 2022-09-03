import copy
import time
import TermTk as ttk
from ..wrk_supervisor import get_started_apps, start_app, stop_app, get_service_pids
from ..meta_about import refresh_about
from ..globals import safestring
from .gvars import *

CREATE_NEW = "START NEW"


def get_apps_services_widget():
    # Get existing apps and services
    state = {'apps': {}, 'apps_list': [], 'choice': "", 'cmd': "", 'name': ''}

    def refresh_state():
        nonlocal state
        apps = get_started_apps()
        state['apps'] = apps
        apps_list = list(apps.keys())
        apps_list.append(CREATE_NEW)
        state['apps_list'] = apps_list
    refresh_state()
    
    # Generate widgets
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)
    scrollArea = ttk.TTkScrollArea(parent=None, border=0, minHeight=25)
    wrap_widg.layout().addWidget(scrollArea)
    l = 2; ls = 20
    r = 25; rs = 90 
    row = 1 

    ttk.TTkLabel(text='App / Service', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    app_select = ttk.TTkComboBox(list=state['apps_list'], pos=(r,row), size=(rs,1))
    scrollArea.viewport().addWidget(app_select)

    row+=2; ttk.TTkLabel(text='Command', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    cmd_inp = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1))
    scrollArea.viewport().addWidget(cmd_inp)

    row+=2; name_lab = ttk.TTkLabel(text='Name', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    name_inp = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1))
    scrollArea.viewport().addWidget(name_inp)

    row+=2; msg_lab = ttk.TTkLabel(text='', color=ERROR_COLOR, pos=(r,row), size=(rs,1), parent=scrollArea.viewport())

    # Buttons
    row+=2; remove_btn = ttk.TTkButton(text='Remove', pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    remove_btn.setBorderColor(TTkColor.fg('#f20e0a'))
    row+=14; btn_cancel = ttk.TTkButton(text='Cancel', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=False)
    btn_save = ttk.TTkButton(text='Save', pos=(r,row), size=(rs,1), parent=scrollArea.viewport(), visible=False)

    def appSelectHandler(i):
        nonlocal state
        refresh_state()
        app_select._list = state['apps_list']; app_select.update()
        choice = state['apps_list'][i]
        state['choice'] = choice
        msg_lab._color = ERROR_COLOR; msg_lab._text = ""; msg_lab.update()
        if choice != CREATE_NEW:
            name_inp._text = choice; name_inp.update() 
            cmd = state['apps'][choice]
            cmd_inp._text = cmd; cmd_inp.update()
            # Show delete, cancel and save buttons
            btn_cancel.hide()
            btn_save.hide()
            remove_btn.show()
        else:
            remove_btn.hide()
            btn_cancel.show()
            btn_save.show()
            cmd_inp._text = ""; cmd_inp.update()
            name_inp._text = ""; name_inp.update()
    app_select.currentIndexChanged.connect(lambda i : appSelectHandler(i))

    # Text input handlers
    def _processCMDInput(n): 
        nonlocal state
        state['cmd'] = n
        msg_lab._color = ERROR_COLOR; msg_lab._text = ""; msg_lab.update()
    def _processNameInput(n): 
        nonlocal state
        state['name'] = n
        msg_lab._color = ERROR_COLOR; msg_lab._text = ""; msg_lab.update()
    # Bind text inputs
    cmd_inp.textEdited.connect(lambda n: _processCMDInput(n))
    name_inp.textEdited.connect(lambda n: _processNameInput(n))

    def _removeBtn(): 
        nonlocal state
        choice = state['choice']
        try:
            stop_app(choice)
        except:
            pass
        time.sleep(2)
        # refresh state
        refresh_state()
        app_select._list = state['apps_list']; app_select.update()
        # refresh about page
        refresh_about()
        # refresh UI & clean inputs
        app_select.setCurrentIndex(-1)
        app_select.update()
        cmd_inp._text = ""; cmd_inp.update()
        name_inp._text = ""; name_inp.update()
    # Bind remove button
    remove_btn.clicked.connect(_removeBtn)

    def _saveBtn(): 
        nonlocal state
        cmd = state['cmd']
        name = safestring(state['name'])
        if cmd == "": 
            msg_lab._color = ERROR_COLOR; msg_lab._text = "Please enter commad to start app or service"; msg_lab.update()
            return
        if name == "": 
            msg_lab._color = ERROR_COLOR; msg_lab._text = "Please give a name for your app or service"; msg_lab.update()
            return
        # Start app/service
        res = start_app(name, cmd)
        # Sleep 3 sec
        msg_lab._color = WAIT_COLOR
        msg_lab._text = "starting..."; msg_lab.update()
        time.sleep(3)
        # Check running 
        pids = get_service_pids(cmd) # <- does not always work!
        # refresh state
        time.sleep(2)
        refresh_state()
        app_select._list = state['apps_list']; app_select.update()
        # refresh about page
        refresh_about()
        # update UI
        app_select.setCurrentIndex(state['apps_list'].index(name))
        app_select.update()
        # cmd_inp._text = name; cmd_inp.update()
        # name_inp._text = state['apps'][name]; name_inp.update()
        # Show success color message
        msg_lab._color = WAIT_COLOR
        msg_lab._text = "Executed"; msg_lab.update()
        return
    # Bind save button
    btn_save.clicked.connect(_saveBtn)

    def _cancelBtn(): 
        nonlocal state
        # refresh state
        refresh_state()
        # refresh UI & clean inputs
        app_select.setCurrentIndex(-1)
        app_select.update()
        cmd_inp._text = ""; cmd_inp.update()
        name_inp._text = ""; name_inp.update()
    btn_cancel.clicked.connect(_cancelBtn)

    return wrap_widg