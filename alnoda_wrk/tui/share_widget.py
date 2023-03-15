import copy
import TermTk as ttk
from TermTk.TTkCore.string import TTkString
from .helper_vidgets import make_horizontal_pair
from .gvars import *
from ..globals import *
from ..fileops import read_ui_conf
from ..share import expose_port


def get_custom_tab():
    """ Expose custom port """
    state = {"internal_port": None}
    scrollArea = ttk.TTkScrollArea(parent=None, border=0, minHeight=22)
    scrollArea.setPadding(0,0,0,2)
    l = 2; ls = 50
    r = 55; rs = 60 
    fs = 100
    row = 1
    ttk.TTkLabel(text='Expose app on port', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    inp_port = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1))
    scrollArea.viewport().addWidget(inp_port)

    # Accept terms
    row+=2; accept_terms_check = ttk.TTkCheckbox(text='Accept terms and conditions', pos=(l,row), size=(fs,1), parent=scrollArea.viewport(), visible=True)

    # Buttons
    row+=2; btn_share = ttk.TTkButton(text='Expose via Internet', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=True)

    # Messages
    row+=2; msg_lab_1 = ttk.TTkLabel(text='', pos=(l,row), size=(fs,1), parent=scrollArea.viewport())
    row+=2; msg_lab_2 = ttk.TTkLabel(text='', pos=(l,row), size=(fs,1), parent=scrollArea.viewport())
    row+=2; msg_lab_3 = ttk.TTkLabel(text='', pos=(l,row), size=(fs,1), parent=scrollArea.viewport())
    row+=2; msg_lab_4 = ttk.TTkLabel(text='', pos=(l,row), size=(fs,1), parent=scrollArea.viewport())

    # Bind text inputs
    def _processPortInput(p): state['internal_port'] = p
    inp_port.textEdited.connect(lambda p: _processPortInput(p))

    def _btnShareHandler():
        # check validity of port to expose
        internal_port = 0
        try: internal_port = int(state['internal_port'])
        except: 
            msg_lab_1._color = ERROR_COLOR; msg_lab_1._text = f"Incorrect port: {state['internal_port']}"; msg_lab_1.update()
            return
        if internal_port < 0 or internal_port > 65353:
            msg_lab_1._color = ERROR_COLOR; msg_lab_1._text = f"Incorrect port: {state['internal_port']}"; msg_lab_1.update()
            return
        # check that terms are accepted
        terms_accepted = accept_terms_check.checkState()
        if not terms_accepted:
            msg_lab_1._color = ERROR_COLOR; msg_lab_1._text = f"Please accept terms"; msg_lab_1.update()
            return
        # Expose port, call API
        succes, extra = expose_port(internal_port)
        # update UI
        if not succes:
            msg_lab_1._color = ERROR_COLOR; msg_lab_1._text = f"Failed! {extra}"; msg_lab_1.update()
            return
        else:
            full_url = extra['full_url']
            session_duration_min = extra['session_duration_min']
            bandwidth_limit = extra['bandwidth_limit']
            max_num_frp_processes = extra['max_num_frp_processes']
            msg_lab_1._text = f"Application is shared over Internet. Share this link with your peer"; msg_lab_1.update()
            msg_lab_2._color = LABEL_COLOR; msg_lab_2._text = full_url; msg_lab_2.update()
            msg_lab_3._text = f"Session {session_duration_min} min, badwidth {bandwidth_limit}"; msg_lab_3.update()
            msg_lab_4._color = ERROR_COLOR; msg_lab_4._text = f"Close admin window to stop sharing"; msg_lab_4.update()
        return
    btn_share.clicked.connect(_btnShareHandler)
    
    return scrollArea




def get_tab_widgets(tab, ui_conf):
    """Create widgets for the specific tab"""
    apps_list = list(ui_conf[tab].keys())
    state = {'choice': None, 'internal_port': None, 'app_data': None}

    def refresh_state():
        state['choice'] = None
        state['internal_port'] = None
        state['app_data'] = None
        msg_lab_1._text = ""; msg_lab_1.update()
        msg_lab_2._text = ""; msg_lab_2.update()
        msg_lab_3._text = ""; msg_lab_3.update()
        msg_lab_4._text = ""; msg_lab_4.update()
        accept_terms_check.setCheckState(False); accept_terms_check.update()
        return

    scrollArea = ttk.TTkScrollArea(parent=None, border=0, minHeight=22)
    scrollArea.setPadding(0,0,0,2)
    l = 2; ls = 50
    r = 55; rs = 60 
    fs = 100
    row = 1
    debt = ttk.TTkLabel(text='Chose app', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    app_select = ttk.TTkComboBox(list=apps_list, pos=(r,row), size=(rs,1))
    scrollArea.viewport().addWidget(app_select)

    # App description
    row+=2; descr_lab = ttk.TTkLabel(text='', pos=(l,row), size=(fs,1), parent=scrollArea.viewport())

    # Accept terms
    row+=2; accept_terms_check = ttk.TTkCheckbox(text='Accept terms and conditions', pos=(l,row), size=(fs,1), parent=scrollArea.viewport(), visible=False)

    # Buttons
    row+=2; btn_share = ttk.TTkButton(text='Share via Internet', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=False)

    # Messages
    row+=2; msg_lab_1 = ttk.TTkLabel(text='', pos=(l,row), size=(fs,1), parent=scrollArea.viewport())
    row+=2; msg_lab_2 = ttk.TTkLabel(text='', pos=(l,row), size=(fs,1), parent=scrollArea.viewport())
    row+=2; msg_lab_3 = ttk.TTkLabel(text='', pos=(l,row), size=(fs,1), parent=scrollArea.viewport())
    row+=2; msg_lab_4 = ttk.TTkLabel(text='', pos=(l,row), size=(fs,1), parent=scrollArea.viewport())
        
    # App Selection handling
    def appSelectHandler(i):
        nonlocal apps_list; nonlocal state
        refresh_state()
        # get app info and store in state
        choice = apps_list[i]
        state['choice'] = choice
        app_data = ui_conf[tab][choice]
        state['app_data'] = app_data
        app_description = app_data['description']
        internal_port = app_data['port']
        state['internal_port'] = internal_port
        # update UI components
        descr_lab._text = str(app_description); descr_lab.update()
        btn_share._visible=True; btn_share.update()
        accept_terms_check._visible=True; accept_terms_check.update()
    app_select.currentIndexChanged.connect(lambda i : appSelectHandler(i))

    # Create new handling
    def _btnShareHandler():
        # check that terms are accepted
        terms_accepted = accept_terms_check.checkState()
        if not terms_accepted:
            msg_lab_1._color = ERROR_COLOR; msg_lab_1._text = f"Please accept terms"; msg_lab_1.update()
            return
        # determine internal port to expose
        internal_port = 0
        try: internal_port = int(state['internal_port'])
        except: 
            msg_lab_1._color = ERROR_COLOR; msg_lab_1._text = f"Application has misconfigured port {state['internal_port']}"; msg_lab_1.update()
            return
        # Expose port, call API
        succes, extra = expose_port(internal_port)
        # update UI
        if not succes:
            msg_lab_1._color = ERROR_COLOR; msg_lab_1._text = f"Failed! {extra}"; msg_lab_1.update()
            return
        else:
            full_url = extra['full_url']
            session_duration_min = extra['session_duration_min']
            bandwidth_limit = extra['bandwidth_limit']
            max_num_frp_processes = extra['max_num_frp_processes']
            msg_lab_1._text = f"Application is shared over Internet. Share this link with your peer"; msg_lab_1.update()
            msg_lab_2._color = LABEL_COLOR; msg_lab_2._text = full_url; msg_lab_2.update()
            msg_lab_3._text = f"Session {session_duration_min} min, badwidth {bandwidth_limit}"; msg_lab_3.update()
            msg_lab_4._color = ERROR_COLOR; msg_lab_4._text = f"Close admin window to stop sharing"; msg_lab_4.update()
        return
    btn_share.clicked.connect(_btnShareHandler)

    return scrollArea



def get_share_widget():
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)
    tabArea = ttk.TTkTabWidget(minHeight=15, border=True)
    wrap_widg.layout().addWidget(tabArea)

    # Read UI conf
    ui_conf = read_ui_conf()

    # Create tabs
    HomeScrollArea = get_tab_widgets("home", ui_conf)
    tabArea.addTab(HomeScrollArea,  "Home")

    try:
        HomeScrollArea = get_tab_widgets("my_apps", ui_conf)
        tabArea.addTab(HomeScrollArea,  "My Apps")
    except:
        pass

    try:
        HomeScrollArea = get_tab_widgets("admin", ui_conf)
        tabArea.addTab(HomeScrollArea,  "Admin")
    except:
        pass
    
    try:
        CustomTabArea = get_custom_tab()
        tabArea.addTab(CustomTabArea,  "Custom")
    except:
        pass

    return wrap_widg



