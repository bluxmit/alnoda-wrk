import TermTk as ttk
import copy
import time
from .gvars import *
from ..zsh import get_user_aliases, add_user_alias, remove_user_alias

CREATE_NEW = "ADD NEW"


def get_aliases_widget():
    state = {'aliases': {}, 'alias_list': [], 'choice': "", 'name': "", 'cmd': ""}

    def refresh_state():
        state['aliases'] = get_user_aliases()
        aliases = state['aliases']
        state['alias_list'] = list(aliases.keys())
        state['alias_list'].append(CREATE_NEW)
    refresh_state()

    # Generate widgets
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)
    scrollArea = ttk.TTkScrollArea(parent=None, border=0, minHeight=25)
    wrap_widg.layout().addWidget(scrollArea)
    l = 2; ls = 20
    r = 25; rs = 90 
    row = 1 

    ttk.TTkLabel(text='alias (terminal)', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    alias_select = ttk.TTkComboBox(list=state['alias_list'], pos=(r,row), size=(rs,1))
    scrollArea.viewport().addWidget(alias_select)

    row+=2; name_inp_lab = ttk.TTkLabel(text='Short name', color=LABEL_COLOR, pos=(l,row), size=(ls,1), visible=False)
    name_inp = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1), visible=False)
    scrollArea.viewport().addWidget(name_inp_lab); scrollArea.viewport().addWidget(name_inp)

    row+=2; cmd_inp_lab = ttk.TTkLabel(text='Command', color=LABEL_COLOR, pos=(l,row), size=(ls,1), visible=False)
    cmd_inp = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1),  visible=False)
    scrollArea.viewport().addWidget(cmd_inp_lab); scrollArea.viewport().addWidget(cmd_inp)
    
    row+=2; msg_lab = ttk.TTkLabel(text='', color=ERROR_COLOR, pos=(r,row), size=(rs,1), parent=scrollArea.viewport())

    # Buttons
    row+=2; remove_btn = ttk.TTkButton(text='Remove', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=False)
    remove_btn.setBorderColor(TTkColor.fg('#f20e0a'))

    row+=12; btn_cancel = ttk.TTkButton(text='Cancel', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=False)
    btn_save = ttk.TTkButton(text='Save', pos=(r,row), size=(rs,1), parent=scrollArea.viewport(), visible=False)

    def aliasSelectHandler(i):
        nonlocal state
        refresh_state()
        choice = state['alias_list'][i]
        state['choice'] = choice
        name_inp_lab.visible=True; name_inp_lab.show(); name_inp_lab.update()
        name_inp.visible=True; name_inp.show(); name_inp.update()
        cmd_inp_lab.visible=True; cmd_inp_lab.show(); cmd_inp_lab.update()
        cmd_inp.visible=True; cmd_inp.show(); cmd_inp.update()
        msg_lab._color = ERROR_COLOR; msg_lab._text = ""; msg_lab.update()
        if choice != CREATE_NEW:
            name_inp._text = choice; name_inp.update() 
            cmd = state['aliases'][choice]
            cmd_inp._text = cmd; cmd_inp.update()
            # Show delete, cancel and save buttons
            btn_cancel.hide()
            btn_save.hide()
            remove_btn.show()
        else:
            remove_btn.hide()
            btn_cancel.show()
            btn_save.show()
            name_inp._text = ""; name_inp.update()
            cmd_inp._text = ""; cmd_inp.update()
    alias_select.currentIndexChanged.connect(lambda i : aliasSelectHandler(i))
    
    # Text input handlers
    def _processNameInput(n): 
        nonlocal state
        state['name'] = n
        msg_lab._color = ERROR_COLOR; msg_lab._text = ""; msg_lab.update()
    def _processcmdInput(n): 
        nonlocal state
        state['cmd'] = n
        msg_lab._color = ERROR_COLOR; msg_lab._text = ""; msg_lab.update()
    # Bind text inputs
    name_inp.textEdited.connect(lambda n: _processNameInput(n))
    cmd_inp.textEdited.connect(lambda n: _processcmdInput(n))

    def _removeBtn(): 
        nonlocal state
        choice = state['choice']
        remove_user_alias(choice)
        # refresh state
        time.sleep(2)
        refresh_state()
        alias_select._list = state['alias_list']; alias_select.update()
        # refresh UI & clean inputs
        alias_select.setCurrentIndex(-1)
        alias_select.update()
        name_inp._text = ""; name_inp.update()
        cmd_inp._text = ""; cmd_inp.update()
        btn_cancel.hide()
        btn_save.hide()
        msg_lab._color = WAIT_COLOR; msg_lab._text = "Please restart terminal to apply changes"; msg_lab.update()
    # Bind remove button
    remove_btn.clicked.connect(_removeBtn)

    def _saveBtn(): 
        nonlocal state
        name = state['name']
        cmd = state['cmd']
        if name == "": 
            msg_lab._color = ERROR_COLOR; msg_lab._text = "Please enter alias short name"; msg_lab.update()
            return
        if cmd == "": 
            msg_lab._color = ERROR_COLOR; msg_lab._text = "Please enter command"; msg_lab.update()
            return
        if not name.isidentifier():
            msg_lab._color = ERROR_COLOR; msg_lab._text = "Alias name is not appropriate (one word, no special chars)"; msg_lab.update()
            return
        # Start app/service
        add_user_alias(name, cmd)
        # refresh state
        time.sleep(2)
        refresh_state()
        alias_select._list = state['alias_list']; alias_select.update()
        # update UI
        alias_select.setCurrentIndex(state['alias_list'].index(name))
        alias_select.update()
        # Show success color message
        msg_lab._color = WAIT_COLOR; msg_lab._text = "Alias added. Please restart terminal to use"; msg_lab.update()
        return
    # Bind save button
    btn_save.clicked.connect(_saveBtn)

    def _cancelBtn(): 
        nonlocal state
        # refresh state
        refresh_state()
        # refresh UI & clean inputs
        alias_select.setCurrentIndex(-1)
        alias_select.update()
        name_inp._text = ""; name_inp.update()
        cmd_inp._text = ""; cmd_inp.update()
    btn_cancel.clicked.connect(_cancelBtn)

    return wrap_widg
