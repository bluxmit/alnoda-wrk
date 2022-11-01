import TermTk as ttk
import copy
import time
from .helper_vidgets import get_file_viewer
from .gvars import *
from ..globals import get_code
from ..processes import *

CREATE_NEW = "START NEW"


def get_processes_widget():
    state = {'processes': {}, 'widgets': [], 'new_cmd': "", 'new_name': "", 'new_flags': ""}

    def refresh_state():
        procs, pnames = get_processes()
        processes = {}
        for p in procs:
            pname = p['name']
            processes[pname] = {}
            processes[pname]['status'] = p['pm2_env']['status']
            processes[pname]['stdout_log'] = p['pm2_env']['pm_out_log_path']
            processes[pname]['stderr_log'] = p['pm2_env']['pm_err_log_path'] 
            processes[pname]['cpu'] = p['monit']['cpu'] 
            processes[pname]['memory'] = p['monit']['memory'] 
        state['processes'] = processes
        state['widgets'] = []
        state['new_cmd'] = ""
        state['new_name'] = ""
        state['new_flags'] = ""
        return
    refresh_state()

    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)
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
            stop_process(name)
            # remove widgets 
            remove_all_widgets()
            # generate new state
            refresh_state()
            # generate section view widgets again
            create_process_widgets()
        return _StopBtn
    def get_stdout_handler(stdout_path):
        nonlocal wrap_widg
        def _stdoutBtn():
            nonlocal wrap_widg
            fw = get_file_viewer(stdout_path, wrap_widg)
        return _stdoutBtn
    def get_stderr_handler(stderr_path):
        nonlocal wrap_widg
        def _stderrBtn():
            nonlocal wrap_widg
            fw = get_file_viewer(stderr_path, wrap_widg)
        return _stderrBtn
    def create_process_widgets():
        nonlocal state
        row = 1
        for name, vals in state['processes'].items():
            # read process params from state
            status = vals['status']
            stdout_log = vals['stdout_log']
            stderr_log = vals['stderr_log'] 
            cpu = vals['cpu'] 
            memory = vals['memory']
            # generate widgets
            name_lab = ttk.TTkLabel(text='process name:', color=LABEL_COLOR, pos=(l,row), size=(ls,1))
            V.addWidget(name_lab); state['widgets'].append(name_lab)
            stop_btn = ttk.TTkButton(text='Stop', pos=(r,row), size=(20,1), visible=True)
            stop_btn.setBorderColor(TTkColor.fg('#f20e0a')); row += 1  
            V.addWidget(stop_btn); state['widgets'].append(stop_btn)
            stop_btn.clicked.connect(get_stop_handler(name))
            w_name = ttk.TTkLineEdit(text=name, pos=(l,row), size=(ls,1)) 
            if status in ['online']:
                status_lab = ttk.TTkLabel(text=status, color=SUCCESS_COLOR, pos=(r,row), size=(rs,1))
            else:
                status_lab = ttk.TTkLabel(text=status, color=ERROR_COLOR, pos=(r,row), size=(rs,1))
            V.addWidget(w_name); V.addWidget(status_lab); row += 1
            state['widgets'].append(w_name); state['widgets'].append(status_lab)
            # Logs buttons
            stdout_log_btn = ttk.TTkButton(text='std.out logs', pos=(l,row), size=(ls,1), visible=True) 
            stderr_log_btn = ttk.TTkButton(text='std.error logs', pos=(r,row), size=(rs,1), visible=True)
            V.addWidget(stdout_log_btn); V.addWidget(stderr_log_btn); row += 2
            state['widgets'].append(stdout_log_btn); state['widgets'].append(stderr_log_btn)
            stdout_log_btn.clicked.connect(get_stdout_handler(stdout_log))
            stderr_log_btn.clicked.connect(get_stderr_handler(stderr_log))    
            row += 1

        # New Process
        if len(state['processes']) > 0: row += 2
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
            new_cmd = state['new_cmd']
            new_name = state['new_name']
            new_flags = state['new_flags']
            if new_cmd == "":
                msg_lab._text = "Please enter command"; msg_lab.visible=True; msg_lab.show(); msg_lab.update()
                return
            if new_name == "":
                msg_lab._text = "Please enter process name"; msg_lab.visible=True; msg_lab.show(); msg_lab.update()
                return
            if new_name in list(state['processes'].keys()):
                msg_lab._text = "Process with this name is already present"; msg_lab.visible=True; msg_lab.show(); msg_lab.update()
                return
            # start with PM2
            start_process(name=new_name, cmd=new_cmd, flags=new_flags)
            # remove remove_all_widgets 
            remove_all_widgets()
            # generate new state
            refresh_state()
            # generate section view widgets again
            create_process_widgets()
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
