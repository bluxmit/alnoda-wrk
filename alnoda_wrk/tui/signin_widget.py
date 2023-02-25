import TermTk as ttk
import copy
import time
from .gvars import *
from ..sign_in import *


def get_signin_widget():
    state = {'auth': {}, 'token': "", 'new_token': "", 'username': "", 'authenticated': False}

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

    def generate_vidgets():
        # Generate widgets
        wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)
        scrollArea = ttk.TTkScrollArea(parent=None, border=0, minHeight=25)
        wrap_widg.layout().addWidget(scrollArea)
        l = 2; ls = 20
        r = 25; rs = 90 
        row = 1 

        if state['authenticated']:
            # Make auth components invisible
            # Show authenticated componenets
            ttk.TTkLabel(text=f'Workspace authenticated', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=True)
            row+=2; ttk.TTkLabel(text=f'Hello {state["username"]}', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=True)
            row+=2; signout_btn = ttk.TTkButton(text='Sign out', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=True)

            # Button handler
            def _SignOutBtn(): 
                nonlocal state
                new_token = state['new_token']
                delete_auth()
                time.sleep(1)
                generate_vidgets()
            # Bind signin button
            signout_btn.clicked.connect(_SignOutBtn)
        else:
            # Make authenticated invisible
            # Show auth componenets
            ttk.TTkLabel(text=f'Not authenticated', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=True)
            row+=2; ttk.TTkLabel(text=f'Authenticate to https://alnoda.org', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=True)
            row+=2; token_inp_lab = ttk.TTkLabel(text='Security token', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=True)
            token_inp = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1), parent=scrollArea.viewport(), visible=True)
            row+=2; signin_btn = ttk.TTkButton(text='Authenticate', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=True)
            row+=2; error_lab = ttk.TTkLabel(text='Failed!', color=ERROR_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=False)
            
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
                    generate_vidgets()
                else:
                    error_lab.visible=True; error_lab.show(); error_lab.update()
            # Bind signin button
            signin_btn.clicked.connect(_SignInBtn)

        # finally, return widgets
        return wrap_widg


    wrap_widg = generate_vidgets()
    return wrap_widg
