import os
import copy
import time
import TermTk as ttk
from ..wrk_supervisor import get_started_apps, create_supervisord_file, stop_app, get_service_pids
from ..meta_about import refresh_about
from ..globals import safestring, VAR_LOG_FOLDER
from .helper_vidgets import get_file_viewer
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

    row+=2; cmd_inp_lab = ttk.TTkLabel(text='Command', color=LABEL_COLOR, pos=(l,row), size=(ls,1), visible=False)
    cmd_inp = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1), visible=False)
    scrollArea.viewport().addWidget(cmd_inp_lab); scrollArea.viewport().addWidget(cmd_inp)

    row+=2; name_inp_lab = ttk.TTkLabel(text='Name', color=LABEL_COLOR, pos=(l,row), size=(ls,1), visible=False)
    name_inp = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1), visible=False)
    scrollArea.viewport().addWidget(name_inp_lab); scrollArea.viewport().addWidget(name_inp)

    row+=2; msg_lab = ttk.TTkLabel(text='', color=ERROR_COLOR, pos=(r,row), size=(rs,1), parent=scrollArea.viewport())

    # Logs
    row+=2; stdout_log_btn = ttk.TTkButton(text='std.out logs', pos=(r,row), size=(rs,1), parent=scrollArea.viewport(), visible=False)
    row+=2; stderr_log_btn = ttk.TTkButton(text='std.error logs', pos=(r,row), size=(rs,1), parent=scrollArea.viewport(), visible=False)

    # Buttons
    row+=2; remove_btn = ttk.TTkButton(text='Remove', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=False)
    remove_btn.setBorderColor(TTkColor.fg('#f20e0a'))
    row+=10; btn_cancel = ttk.TTkButton(text='Cancel', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=False)
    btn_save = ttk.TTkButton(text='Save', pos=(r,row), size=(rs,1), parent=scrollArea.viewport(), visible=False)

    def appSelectHandler(i):
        nonlocal state
        refresh_state()
        app_select._list = state['apps_list']; app_select.update()
        choice = state['apps_list'][i]
        state['choice'] = choice

        cmd_inp_lab.visible=True; cmd_inp_lab.show(); cmd_inp_lab.update()
        cmd_inp.visible=True; cmd_inp.show(); cmd_inp.update()
        name_inp_lab.visible=True; name_inp_lab.show(); name_inp_lab.update()
        name_inp.visible=True; name_inp.show(); name_inp.update()

        msg_lab._color = ERROR_COLOR; msg_lab._text = ""; msg_lab.update()
        if choice != CREATE_NEW:
            name_inp._text = choice; name_inp.update() 
            cmd = state['apps'][choice]
            cmd_inp._text = cmd; cmd_inp.update()
            # Show delete, cancel and save buttons
            btn_cancel.hide()
            btn_save.hide()
            remove_btn.show()
            stdout_log_btn.show()
            stderr_log_btn.show()
        else:
            remove_btn.hide()
            stdout_log_btn.hide()
            stderr_log_btn.hide()
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

    def _stderrlogBtn(): 
        nonlocal state
        choice = state['choice']
        file_ = os.path.join(VAR_LOG_FOLDER, f"{choice}-stderr.log")
        fw = get_file_viewer(file_, wrap_widg)
    # Bind stderr log button
    stderr_log_btn.clicked.connect(_stderrlogBtn)

    def _stdoutlogBtn(): 
        nonlocal state
        choice = state['choice']
        file_ = os.path.join(VAR_LOG_FOLDER, f"{choice}-stdout.log")
        fw = get_file_viewer(file_, wrap_widg)
    # Bind stderr log button
    stdout_log_btn.clicked.connect(_stdoutlogBtn)

    def _removeBtn(): 
        nonlocal state
        choice = state['choice']
        stop_app(choice)
        # refresh state
        time.sleep(2)
        refresh_state()
        app_select._list = state['apps_list']; app_select.update()
        # refresh about page
        refresh_about()
        # refresh UI & clean inputs
        app_select.setCurrentIndex(-1)
        app_select.update()
        cmd_inp._text = ""; cmd_inp.update()
        name_inp._text = ""; name_inp.update()
        msg_lab._color = WAIT_COLOR; msg_lab._text = "Restart workspace for changes to take place"; msg_lab.update()
        btn_cancel.hide()
        btn_save.hide()
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
        create_supervisord_file(name, cmd)
        # refresh state
        time.sleep(2)
        refresh_state()
        app_select._list = state['apps_list']; app_select.update()
        # refresh about page
        refresh_about()
        # update UI
        app_select.setCurrentIndex(state['apps_list'].index(name))
        app_select.update()
        # Show success color message
        msg_lab._color = WAIT_COLOR; msg_lab._text = "Restart workspace for changes to take place" 
        msg_lab.update()
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