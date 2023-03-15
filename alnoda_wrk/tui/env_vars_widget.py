import TermTk as ttk
import copy
import time
from .gvars import *
from ..zsh import get_user_env_vars, add_user_env_var, remove_user_env_var

CREATE_NEW = "ADD NEW"


def get_env_vars_widget():
    state = {'envars': {}, 'vars_list': [], 'choice': "", 'name': "", 'value': ""}

    def refresh_state():
        state['envars'] = get_user_env_vars()
        envars = state['envars']
        state['vars_list'] = list(envars.keys())
        state['vars_list'].append(CREATE_NEW)
    refresh_state()

    # Generate widgets
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)
    scrollArea = ttk.TTkScrollArea(parent=None, border=0, minHeight=25)
    wrap_widg.layout().addWidget(scrollArea)
    l = 2; ls = 20
    r = 25; rs = 90 
    row = 1 

    ttk.TTkLabel(text='env var (terminal)', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    var_select = ttk.TTkComboBox(list=state['vars_list'], pos=(r,row), size=(rs,1))
    scrollArea.viewport().addWidget(var_select)

    row+=2; name_inp_lab = ttk.TTkLabel(text='Name', color=LABEL_COLOR, pos=(l,row), size=(ls,1), visible=False)
    name_inp = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1), visible=False)
    scrollArea.viewport().addWidget(name_inp_lab); scrollArea.viewport().addWidget(name_inp)

    row+=2; value_inp_lab = ttk.TTkLabel(text='Value', color=LABEL_COLOR, pos=(l,row), size=(ls,1), visible=False)
    value_inp = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1), visible=False)
    scrollArea.viewport().addWidget(value_inp_lab); scrollArea.viewport().addWidget(value_inp)
    
    row+=2; msg_lab = ttk.TTkLabel(text='', color=ERROR_COLOR, pos=(r,row), size=(rs,1), parent=scrollArea.viewport())

    # Buttons
    row+=2; remove_btn = ttk.TTkButton(text='Remove', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=False)
    remove_btn.setBorderColor(TTkColor.fg('#f20e0a'))

    row+=12; btn_cancel = ttk.TTkButton(text='Cancel', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=False)
    btn_save = ttk.TTkButton(text='Save', pos=(r,row), size=(rs,1), parent=scrollArea.viewport(), visible=False)

    def varSelectHandler(i):
        nonlocal state
        refresh_state()
        choice = state['vars_list'][i]
        state['choice'] = choice
        name_inp_lab.visible=True; name_inp_lab.show(); name_inp_lab.update()
        name_inp.visible=True; name_inp.show(); name_inp.update()
        value_inp_lab.visible=True; value_inp_lab.show(); value_inp_lab.update()
        value_inp.visible=True; value_inp.show(); value_inp.update()
        msg_lab._color = ERROR_COLOR; msg_lab._text = ""; msg_lab.update()
        if choice != CREATE_NEW:
            name_inp._text = choice; name_inp.update() 
            value = state['envars'][choice]
            value_inp._text = value; value_inp.update()
            # Show delete, cancel and save buttons
            btn_cancel.hide()
            btn_save.hide()
            remove_btn.show()
        else:
            remove_btn.hide()
            btn_cancel.show()
            btn_save.show()
            name_inp._text = ""; name_inp.update()
            value_inp._text = ""; value_inp.update()
    var_select.currentIndexChanged.connect(lambda i : varSelectHandler(i))
    
    # Text input handlers
    def _processNameInput(n): 
        nonlocal state
        state['name'] = n
        msg_lab._color = ERROR_COLOR; msg_lab._text = ""; msg_lab.update()
    def _processValueInput(n): 
        nonlocal state
        state['value'] = n
        msg_lab._color = ERROR_COLOR; msg_lab._text = ""; msg_lab.update()
    # Bind text inputs
    name_inp.textEdited.connect(lambda n: _processNameInput(n))
    value_inp.textEdited.connect(lambda n: _processValueInput(n))

    def _removeBtn(): 
        nonlocal state
        choice = state['choice']
        remove_user_env_var(choice)
        # refresh state
        time.sleep(2)
        refresh_state()
        var_select._list = state['vars_list']; var_select.update()
        # refresh UI & clean inputs
        var_select.setCurrentIndex(-1)
        var_select.update()
        name_inp._text = ""; name_inp.update()
        value_inp._text = ""; value_inp.update()
        btn_cancel.hide()
        btn_save.hide()
        msg_lab._color = WAIT_COLOR; msg_lab._text = "Please restart terminal to apply changes"; msg_lab.update()
    # Bind remove button
    remove_btn.clicked.connect(_removeBtn)

    def _saveBtn(): 
        nonlocal state
        name = state['name']
        value = state['value']
        if name == "": 
            msg_lab._color = ERROR_COLOR; msg_lab._text = "Please enter name for the variable"; msg_lab.update()
            return
        if value == "": 
            msg_lab._color = ERROR_COLOR; msg_lab._text = "Please enter value for the variable"; msg_lab.update()
            return
        if not name.isidentifier():
            msg_lab._color = ERROR_COLOR; msg_lab._text = "Variable name is not appropriate"; msg_lab.update()
            return
        # Start app/service
        add_user_env_var(name, value)
        # refresh state
        time.sleep(2)
        refresh_state()
        var_select._list = state['vars_list']; var_select.update()
        # update UI
        var_select.setCurrentIndex(state['vars_list'].index(name))
        var_select.update()
        # Show success color message
        msg_lab._color = WAIT_COLOR; msg_lab._text = "Variable added. Please restart terminal to use"; msg_lab.update()
        return
    # Bind save button
    btn_save.clicked.connect(_saveBtn)

    def _cancelBtn(): 
        nonlocal state
        # refresh state
        refresh_state()
        # refresh UI & clean inputs
        var_select.setCurrentIndex(-1)
        var_select.update()
        name_inp._text = ""; name_inp.update()
        value_inp._text = ""; value_inp.update()
    btn_cancel.clicked.connect(_cancelBtn)

    return wrap_widg
