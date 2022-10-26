import TermTk as ttk
import copy
import time
from .gvars import *
from ..globals import get_code
from ..cheatsheet import *

CREATE_NEW = "ADD NEW"


def get_cheatsheet_widget():
    superstate = {'selected_section': "", 'mode': ""}
    state = {'cheatsheet_dict': {}, 'cheatsheet_dict_new': {}, 'sections': [], 'widgets': [], 'new_cmd': "", 'new_descr': "", "updates": {}, "new_section_name": "", "updated_section_name": ""}

    def refresh_state():
        state['cheatsheet_dict'] = read_cheatsheet_data()
        state['cheatsheet_dict_new'] = copy.deepcopy(state['cheatsheet_dict']) 
        state['sections'] = list(state['cheatsheet_dict_new'].keys())
        state['widgets'] = []
        state['updates'] = {}
        state['new_cmd'] = ""
        state['new_descr'] = ""
        state['new_section_name'] = ""
        state['updated_section_name'] = ""
    refresh_state()

    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)
    scrollArea = ttk.TTkScrollArea(parent=None, border=0, minHeight=25)
    wrap_widg.layout().addWidget(scrollArea)
    l = 2; ls = 50
    r = 55; rs = 60 
    fs = 100

    debt = ttk.TTkLabel(text='Chose section', color=LABEL_COLOR, pos=(l,1), size=(20,1), parent=scrollArea.viewport())
    main_selector = ttk.TTkComboBox(list=[CREATE_NEW]+state['sections'], pos=(25,1), size=(90,1))
    V = scrollArea.viewport(); V.addWidget(main_selector) 

    def remove_all_widgets():
        for w in state['widgets']:
            V.removeWidget(w)

    def set_main_selector(pos=None):
        nonlocal main_selector
        choices = [CREATE_NEW]+state['sections']
        main_selector._list = choices; main_selector.update()
        ind = 0
        if pos is not None: ind = choices.index(pos)
        main_selector.setCurrentIndex(ind)
        main_selector.update()


    # Text input handlers
    def get_update_cmd_hadler(code):
        def _processUpdateCmdInput(n): 
            nonlocal state; nonlocal debt
            if code not in state['updates']: state['updates'][code] = {}
            state['updates'][code]['upd_cmd'] = n
        return _processUpdateCmdInput
    def get_update_descr_hadler(code): 
        def _processUpdateDescrInput(n): 
            nonlocal state
            if code not in state['updates']: state['updates'][code] = {}
            state['updates'][code]['upd_descr'] = n 
        return _processUpdateDescrInput
    def get_rem_handler(section, code):
        def _removeBtn():
            nonlocal state
            # remove command from cheatsheet
            remove_cheatsheet_command(section, code)
            # remove widgets 
            remove_all_widgets()
            # generate new state
            refresh_state()
            # generate section view widgets again
            create_section_view_widgets(section)
        return _removeBtn
    def get_upd_handler(section, code):
        def _updateBtn():
            nonlocal state
            cmd = None; description = None
            try: cmd = state['updates'][code]['upd_cmd']
            except: pass
            try: description = state['updates'][code]['upd_descr']
            except: pass
            update_cheatsheet_command(section, code, cmd=cmd, description=description)
            # remove widgets 
            remove_all_widgets()
            # generate new state
            refresh_state()
            # generate section view widgets again
            create_section_view_widgets(section)
        return _updateBtn

    def create_section_view_widgets(section):
        nonlocal state
        row = 4
        chap_lab = ttk.TTkLabel(text='MANAGE ITEMS', color=SECTION_COLOR, pos=(l,row), size=(ls,1))
        V.addWidget(chap_lab); state['widgets'].append(chap_lab); row += 2
        for code,d in state['cheatsheet_dict'][section].items():
            cmd = d['cmd']; description = d['description']
            cmd_lab = ttk.TTkLabel(text='command:', color=LABEL_COLOR, pos=(l,row), size=(ls,1))
            descr_lab = ttk.TTkLabel(text='description:', color=LABEL_COLOR, pos=(r,row), size=(rs,1))
            V.addWidget(cmd_lab); V.addWidget(descr_lab); row += 1
            w_cmd = ttk.TTkLineEdit(text=cmd, pos=(l,row), size=(ls,1))
            w_descr = ttk.TTkLineEdit(text=description, pos=(r,row), size=(rs,1))
            V.addWidget(w_cmd); V.addWidget(w_descr); row += 1
            remove_btn = ttk.TTkButton(text='Remove', pos=(l,row), size=(20,1), visible=True)
            remove_btn.setBorderColor(TTkColor.fg('#f20e0a'))
            update_btn = ttk.TTkButton(text='Update', pos=(r,row), size=(20,1), visible=True)
            V.addWidget(remove_btn); V.addWidget(update_btn); row += 2
            state['widgets'].append(cmd_lab); state['widgets'].append(descr_lab) 
            state['widgets'].append(w_cmd); state['widgets'].append(w_descr) 
            state['widgets'].append(remove_btn); state['widgets'].append(update_btn)

            # Bind text inputs
            w_cmd_hand = get_update_cmd_hadler(code)
            w_descr_hand = get_update_descr_hadler(code)
            w_cmd.textEdited.connect(w_cmd_hand)
            w_descr.textEdited.connect(w_descr_hand)

            # Button handlers
            remove_btn.clicked.connect(get_rem_handler(section, code))
            update_btn.clicked.connect(get_upd_handler(section, code))

        # New cheatsheet entry widgets
        new_cmd_lab = ttk.TTkLabel(text='new command:', color=LABEL_COLOR, pos=(l,row), size=(ls,1))
        new_descr_lab = ttk.TTkLabel(text='new description:', color=LABEL_COLOR, pos=(r,row), size=(rs,1))
        V.addWidget(new_cmd_lab); V.addWidget(new_descr_lab); row += 1
        new_w_cmd = ttk.TTkLineEdit(text="", pos=(l,row), size=(ls,1))
        new_w_descr = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1))
        V.addWidget(new_w_cmd); V.addWidget(new_w_descr); row += 1
        new_cancel_btn = ttk.TTkButton(text='Cancel', pos=(l,row), size=(20,1), visible=True)
        new_add_btn = ttk.TTkButton(text='Add', pos=(r,row), size=(20,1), visible=True)
        V.addWidget(new_cancel_btn); V.addWidget(new_add_btn); row += 1
        msg_lab = ttk.TTkLabel(text='', color=ERROR_COLOR, pos=(l,row), size=(fs,1), visible=False)
        V.addWidget(msg_lab)
        state['widgets'].append(new_cmd_lab); state['widgets'].append(new_descr_lab)
        state['widgets'].append(new_w_cmd); state['widgets'].append(new_w_descr)
        state['widgets'].append(new_cancel_btn); state['widgets'].append(new_add_btn)
        state['widgets'].append(msg_lab)

        # Text input handlers
        def _processCmdInput(n): 
            nonlocal state; state['new_cmd'] = n
        def _processDescrInput(n): 
            nonlocal state; state['new_descr'] = n
        # Bind text inputs
        new_w_cmd.textEdited.connect(lambda n: _processCmdInput(n))
        new_w_descr.textEdited.connect(lambda n: _processDescrInput(n))

        # Button handlers
        def _addCmdDescrBtn():
            nonlocal state
            if state['new_cmd'] == "":
                msg_lab._text = "Please enter command"; msg_lab.visible=True; msg_lab.show(); msg_lab.update()
                return
            if state['new_descr'] == "":
                msg_lab._text = "Please enter description"; msg_lab.visible=True; msg_lab.show(); msg_lab.update()
                return
            # remove command from cheatsheet
            add_cheatsheet_command(section, state['new_cmd'], state['new_descr'])
            # remove widgets 
            remove_all_widgets()
            # generate new state
            refresh_state()
            # generate section view widgets again
            create_section_view_widgets(section)
        new_add_btn.clicked.connect(_addCmdDescrBtn)
        def _addCacelBtn():
            # remove widgets 
            remove_all_widgets()
            # generate new state
            refresh_state()
            # generate section view widgets again
            create_section_view_widgets(section)
        new_cancel_btn.clicked.connect(_addCacelBtn)

        # Remove section button
        row += 2
        chap_lab_s = ttk.TTkLabel(text='MANAGE SECTION', color=SECTION_COLOR, pos=(l,row), size=(ls,1))
        V.addWidget(chap_lab_s); state['widgets'].append(chap_lab_s); 
        row += 2
        msk_lab = ttk.TTkLabel(text='section name:', color=LABEL_COLOR, pos=(l,row), size=(ls,1))
        V.addWidget(msk_lab); state['widgets'].append(msk_lab)
        row += 1
        sec_name_inp = ttk.TTkLineEdit(text=section, pos=(l,row), size=(ls,1))     
        V.addWidget(sec_name_inp); state['widgets'].append(sec_name_inp)   
        section_rem_btn = ttk.TTkButton(text='Remove section', pos=(r,row), size=(rs,1), visible=True)
        section_rem_btn.setBorderColor(TTkColor.fg('#f20e0a'))
        V.addWidget(section_rem_btn); state['widgets'].append(section_rem_btn)
        row += 1
        section_name_upd_btn = ttk.TTkButton(text='Update', pos=(l,row), size=(20,1), visible=True)
        V.addWidget(section_name_upd_btn); state['widgets'].append(section_name_upd_btn)
        row += 2
        upd_err_lab = ttk.TTkLabel(text='', color=ERROR_COLOR, pos=(l,row), size=(fs,1), visible=False)
        V.addWidget(upd_err_lab); state['widgets'].append(upd_err_lab)
        # Text input handlers
        def _processNewSectionNameInput(n): 
            nonlocal state; state['updated_section_name'] = n
        # Bind text inputs
        sec_name_inp.textEdited.connect(lambda n: _processNewSectionNameInput(n))
        # Remove button handler
        def _UpdateSectionNameBtn():
            new_name = state['updated_section_name']
            if len(new_name) == 0:
                upd_err_lab._text = "Please enter section name"; upd_err_lab.visible=True; upd_err_lab.show(); upd_err_lab.update()
                return
            rename_cheatsheet_section(section, new_name)
            # remove widgets 
            remove_all_widgets()
            # generate new state
            refresh_state()
            # reset main select
            set_main_selector(new_name)
        section_name_upd_btn.clicked.connect(_UpdateSectionNameBtn)

        # Remove button handler
        def _RemoveSectionBtn():
            # remove entire section
            remove_cheatsheet_section(section)
            # remove widgets 
            remove_all_widgets()
            # generate new state
            refresh_state()
            # unset main selector 
            set_main_selector()
            # main_selector.setCurrentIndex(-1)
        section_rem_btn.clicked.connect(_RemoveSectionBtn)
        row += 1
        fin_lab = ttk.TTkLabel(text='', color=LABEL_COLOR, pos=(l,row), size=(ls,1))
        V.addWidget(fin_lab); state['widgets'].append(fin_lab)


    def create_new_section_input_widgets():
        nonlocal state
        row = 3
        new_section_lab = ttk.TTkLabel(text='section name:', color=LABEL_COLOR, pos=(l,row), size=(20,1))
        new_section_name = ttk.TTkLineEdit(text="", pos=(25,row), size=(90,1))
        V.addWidget(new_section_lab); state['widgets'].append(new_section_lab)
        V.addWidget(new_section_name); state['widgets'].append(new_section_name)
        row += 2
        new_section_btn = ttk.TTkButton(text='Create', pos=(l,row), size=(20,1), visible=True)
        V.addWidget(new_section_btn); state['widgets'].append(new_section_btn)
        row += 2
        err_lab = ttk.TTkLabel(text='', color=ERROR_COLOR, pos=(l,row), size=(fs,1), visible=False)
        V.addWidget(err_lab); state['widgets'].append(err_lab)
        # Text input handlers
        def _processNewSectionInput(n): 
            nonlocal state
            state['new_section_name'] = n
            err_lab._color = ERROR_COLOR; err_lab._text = ""; err_lab.update()
        new_section_name.textEdited.connect(lambda n: _processNewSectionInput(n))
        # Create button hadler
        def _createSectionBtn():
            nonlocal state
            section = state['new_section_name']
            if section == "":
                err_lab._text = "Please enter section name"; err_lab.visible=True; err_lab.show(); err_lab.update()
                return
            add_cheatsheet_section(section)
            # remove widgets 
            remove_all_widgets()
            # generate new state
            refresh_state()
            # update main selector 
            set_main_selector(section)
            # main_selector.setCurrentIndex(state['sections'].index(section))
            # create section widgets
            # create_section_view_widgets(section)
        new_section_btn.clicked.connect(_createSectionBtn)
        
        
    def MainSelectHandler(i):
        nonlocal state; nonlocal superstate
        remove_all_widgets()
        choices = [CREATE_NEW]+state['sections']
        choice = choices[i]
        try:
            selected_section = state['sections'][i-1]
            superstate['selected_section'] = selected_section
        except:
            pass
        if choice != CREATE_NEW:
            superstate['mode'] = "section-view"
            refresh_state(); create_section_view_widgets(choice)
        else:
            superstate['mode'] = "section-new"
            create_new_section_input_widgets()
    main_selector.currentIndexChanged.connect(lambda i : MainSelectHandler(i))

   
    return wrap_widg
