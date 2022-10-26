import TermTk as ttk
import copy
import time
from .gvars import *
from ..globals import get_code

CREATE_NEW = "START NEW"


def get_processes_widget():
    state = {'processes': {}, 'widgets': [], 'new_cmd': "", 'new_name': "", 'new_flags': ""}

    def refresh_state():
        # state['processes'] = get_pm2_processes()  # not implemented 
        state['widgets'] = []
        state['new_cmd'] = ""
        state['new_name'] = ""
        state['new_flags'] = ""
        return
    refresh_state()

    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=True)
    scrollArea = ttk.TTkScrollArea(parent=None, border=0, minHeight=25)
    wrap_widg.layout().addWidget(scrollArea)
    l = 2; ls = 50
    r = 55; rs = 60 
    fs = 113
    V = scrollArea.viewport()

    def remove_all_widgets():
        for w in state['widgets']:
            V.removeWidget(w)

    def get_stop_handler(name):
        def _StopBtn():
            nonlocal state
            # stop process with pm2
            
            # remove widgets 
            remove_all_widgets()
            # generate new state
            refresh_state()
            # generate section view widgets again
            create_process_widgets()
        return _StopBtn

    def create_process_widgets():
        nonlocal state
        row = 1
        for name, cmd in state['processes'].items():
            cmd_lab = ttk.TTkLabel(text='command:', color=LABEL_COLOR, pos=(l,row), size=(ls,1))
            name_lab = ttk.TTkLabel(text='process name:', color=LABEL_COLOR, pos=(r,row), size=(rs,1))
            V.addWidget(cmd_lab); V.addWidget(name_lab); row += 1
            state['widgets'].append(cmd_lab); state['widgets'].append(name_lab) 
            w_cmd = ttk.TTkLineEdit(text=cmd, pos=(l,row), size=(ls,1))
            w_name = ttk.TTkLineEdit(text=name, pos=(r,row), size=(rs,1))
            V.addWidget(w_cmd); V.addWidget(w_name); row += 1
            state['widgets'].append(w_cmd); state['widgets'].append(w_name)
            stop_btn = ttk.TTkButton(text='Stop', pos=(l,row), size=(20,1), visible=True)
            stop_btn.setBorderColor(TTkColor.fg('#f20e0a'))
            V.addWidget(stop_btn); state['widgets'].append(stop_btn)
            # Button handlers
            stop_btn.clicked.connect(get_stop_handler(name))

        # New Process 
        new_cmd_lab = ttk.TTkLabel(text='new command:', color=LABEL_COLOR, pos=(l,row), size=(ls,1))
        new_name_lab = ttk.TTkLabel(text='new process name:', color=LABEL_COLOR, pos=(r,row), size=(rs,1))
        V.addWidget(new_cmd_lab); V.addWidget(new_name_lab); row += 1
        state['widgets'].append(new_cmd_lab); state['widgets'].append(new_name_lab)
        new_w_cmd = ttk.TTkLineEdit(text="", pos=(l,row), size=(ls,1))
        new_w_name = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1))
        V.addWidget(new_w_cmd); V.addWidget(new_w_name); row += 1
        state['widgets'].append(new_w_cmd); state['widgets'].append(new_w_name)
        new_flags_lab = ttk.TTkLabel(text='new command flags:', color=LABEL_COLOR, pos=(l,row), size=(fs,1)); row += 1
        new_w_flags = ttk.TTkLineEdit(text="", pos=(l,row), size=(fs,1)); row += 1
        V.addWidget(new_flags_lab); V.addWidget(new_w_flags)
        state['widgets'].append(new_flags_lab); state['widgets'].append(new_w_flags)

        new_cancel_btn = ttk.TTkButton(text='Cancel', pos=(l,row), size=(20,1), visible=True)
        new_start_btn = ttk.TTkButton(text='Start', pos=(r,row), size=(20,1), visible=True)
        V.addWidget(new_cancel_btn); V.addWidget(new_start_btn); row += 1
        state['widgets'].append(new_cancel_btn); state['widgets'].append(new_start_btn)
        msg_lab = ttk.TTkLabel(text='', color=ERROR_COLOR, pos=(l,row), size=(fs,1), visible=False)
        V.addWidget(msg_lab); state['widgets'].append(msg_lab)
        # Text input handlers
        def _processCmdInput(n): 
            nonlocal state; state['new_cmd'] = n
        def _processNameInput(n): 
            nonlocal state; state['new_name'] = n
        def _processFlagsInput(n): 
            nonlocal state; state['new_flags'] = n
        # Bind text inputs
        new_w_cmd.textEdited.connect(lambda n: _processCmdInput(n))
        new_w_name.textEdited.connect(lambda n: _processNameInput(n))
        new_w_flags.textEdited.connect(lambda n: _processFlagsInput(n))

        # Button handlers
        def _startProcessBtn():
            nonlocal state
            if state['new_cmd'] == "":
                msg_lab._text = "Please enter command"; msg_lab.visible=True; msg_lab.show(); msg_lab.update()
                return
            if state['new_name'] == "":
                msg_lab._text = "Please enter process name"; msg_lab.visible=True; msg_lab.show(); msg_lab.update()
                return
            if state['new_name'] in list(state['processes'].keys()):
                msg_lab._text = "Process with this name is already present"; msg_lab.visible=True; msg_lab.show(); msg_lab.update()
                return
            # start with PM2
            #   <- not implemented
            # remove widgets 
            remove_all_widgets()
            # generate new state
            refresh_state()
            # generate section view widgets again
            create_section_view_widgets(section)
        new_start_btn.clicked.connect(_startProcessBtn)
        def _addCacelBtn():
            nonlocal state
            # clear new process input widgets 
            new_w_cmd._text = ""; new_w_cmd.update()
            new_w_name._text = ""; new_w_name.update()
            new_w_flags._text = ""; new_w_flags.update()
            state['new_cmd'] = ""
            state['new_name'] = ""
            state['new_flags'] = ""
        new_cancel_btn.clicked.connect(_addCacelBtn)

    create_process_widgets()
    return wrap_widg
