import TermTk as ttk
import copy
import time
from .gvars import *
from ..sign_in import *


def get_signin_widget():
    state = {'auth': {}, 'token': "", 'new_token': "", 'username': "", 'authenticated': False, "widgets": []}

    def refresh_state():
        state['auth'] = read_auth()
        try:   
            # if auth file is present:
            state['token'] = state['auth']['token']
            state['username'] = state['auth']['username']
            state['authenticated'] = True
        except: pass
        token = ""
    refresh_state()

    def remove_all_widgets():
        for w in state['widgets']:
            V.removeWidget(w)
        state['widgets'] = []

    # Generate widgets
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)
    scrollArea = ttk.TTkScrollArea(parent=None, border=0, minHeight=25)
    wrap_widg.layout().addWidget(scrollArea)
    V = scrollArea.viewport()
    
    def draw_auth_widgets():
        l = 2; ls = 20
        r = 25; rs = 90 
        row = 1 
        ### WIDGETS IF AUTHENTICATED
        auth_lab = ttk.TTkLabel(text=f'Workspace authenticated', pos=(l,row), size=(ls,1), visible=True)
        row+=2; username_lab = ttk.TTkLabel(text=f'Hello {state["username"]}', pos=(l,row), size=(ls,1), visible=True)
        row+=2; signout_btn = ttk.TTkButton(text='Sign out', pos=(l,row), size=(ls,1), visible=True)
        siged_widgets = [auth_lab, username_lab, signout_btn]; state['widgets'] = state['widgets'] + siged_widgets
        for widget in siged_widgets: V.addWidget(widget)
        # Button handler
        def _SignOutBtn(): 
            nonlocal state
            new_token = state['new_token']
            delete_auth()
            time.sleep(1)
            remove_all_widgets()
            draw_not_auth_widgets()
        # Bind signin button
        signout_btn.clicked.connect(_SignOutBtn)

    def draw_not_auth_widgets():
        l = 2; ls = 20
        r = 25; rs = 90 
        row = 1 
        ### WIDGETS IF NOT AUTHENTICATED
        not_auth_lab = ttk.TTkLabel(text=f'Not authenticated', pos=(l,row), size=(ls,1), visible=True)
        row+=2; auth_to_lab = ttk.TTkLabel(text=f'Authenticate to https://alnoda.org', pos=(l,row), size=(ls,1), visible=True)
        row+=2; token_inp_lab = ttk.TTkLabel(text='Security token', color=LABEL_COLOR, pos=(l,row), size=(ls,1), visible=True)
        token_inp = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1), visible=True)
        row+=2; signin_btn = ttk.TTkButton(text='Authenticate', pos=(l,row), size=(ls,1), visible=True)
        row+=2; error_lab = ttk.TTkLabel(text='Failed', color=ERROR_COLOR, pos=(l,row), size=(ls,1), visible=False)
        not_siged_widgets = [not_auth_lab, auth_to_lab, token_inp_lab, token_inp, signin_btn, error_lab]; state['widgets'] = state['widgets'] + not_siged_widgets
        for widget in not_siged_widgets: V.addWidget(widget)
            # Text input handlers
        def _processTokenInput(n): 
            nonlocal state
            state['new_token'] = n
        token_inp.textEdited.connect(lambda n: _processTokenInput(n))

        # Button handler
        def _SignInBtn(): 
            nonlocal state
            new_token = state['new_token']
            success = add_token(new_token)
            if success:
                remove_all_widgets()
                draw_auth_widgets()
            else:
                error_lab.visible=True; error_lab.show(); error_lab.update()
        # Bind signin button
        signin_btn.clicked.connect(_SignInBtn)

    if state['authenticated']:
        draw_auth_widgets()
    else:
        draw_not_auth_widgets()

    return wrap_widg
