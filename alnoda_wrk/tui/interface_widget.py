import copy
import TermTk as ttk
from TermTk.TTkCore.string import TTkString
from .helper_vidgets import make_horizontal_pair
from .gvars import *
from ..globals import *
from ..fileops import read_ui_conf, update_ui_conf
from ..ui_builder import copy_pageapp_image
from ..meta_about import refresh_from_meta

CREATE_NEW = "CREATE NEW"


def find_title_in_dict(dic, title):
    """
    """
    for k,v in dic.items():
        if v['title'] == title: 
            return v
    # if not found
    app_name = safestring(title)
    new = {'title': "", 'description': "", 'port': "", 'image': "", 'path': ""}
    dic[app_name] = new
    return new


def get_tab_widgets(tab, ui_conf):
    """Create widgets for the specific tab"""
    new_ui_conf = copy.deepcopy(ui_conf)
    apps_list = list(new_ui_conf[tab].keys())
    apps_list.append(CREATE_NEW)
    extra = {'choice': ""}
    new_app = {}

    scrollArea = ttk.TTkScrollArea(parent=None, border=0, minHeight=22)
    scrollArea.setPadding(0,0,0,2)
    l = 2; ls = 50
    r = 55; rs = 60 
    row = 1
    debt = ttk.TTkLabel(text='Chose app', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    app_select = ttk.TTkComboBox(list=apps_list, pos=(r,row), size=(rs,1))
    scrollArea.viewport().addWidget(app_select)

    row+=2; inp_title_lab = ttk.TTkLabel(text='Title', color=LABEL_COLOR, pos=(l,row), size=(ls,1), visible=False)
    inp_title = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1), visible=False)
    scrollArea.viewport().addWidget(inp_title_lab); scrollArea.viewport().addWidget(inp_title)

    row+=2; inp_descr_lab = ttk.TTkLabel(text='Description', color=LABEL_COLOR, pos=(l,row), size=(ls,1), visible=False)
    inp_descr = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1), visible=False)
    scrollArea.viewport().addWidget(inp_descr_lab); scrollArea.viewport().addWidget(inp_descr)

    row+=2; inp_port_lab = ttk.TTkLabel(text='Port (range 8021-8040)', color=LABEL_COLOR, pos=(l,row), size=(ls,1), visible=False)
    inp_port = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1), visible=False)
    scrollArea.viewport().addWidget(inp_port_lab); scrollArea.viewport().addWidget(inp_port)

    row+=2; inp_img_lab = ttk.TTkLabel(text='Image', color=LABEL_COLOR, pos=(l,row), size=(ls,1), visible=False)
    inp_img = ttk.TTkButton(text="", pos=(r,row), size=(rs,1), visible=False)
    scrollArea.viewport().addWidget(inp_img_lab); scrollArea.viewport().addWidget(inp_img)

    row+=2; inp_path_lab = ttk.TTkLabel(text='Path (optional)', color=LABEL_COLOR, pos=(l,row), size=(ls,1), visible=False)
    inp_path = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1), visible=False)
    scrollArea.viewport().addWidget(inp_path_lab); scrollArea.viewport().addWidget(inp_path)

    row+=2; msg_lab = ttk.TTkLabel(text='', color=ERROR_COLOR, pos=(r,row), size=(rs,1), parent=scrollArea.viewport())

    # Buttons
    row+=2; btn_delete = ttk.TTkButton(text='Delete', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=False)
    btn_delete.setBorderColor(TTkColor.fg('#f20e0a'))
    row+=6; btn_cancel = ttk.TTkButton(text='Cancel', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=False)
    btn_save = ttk.TTkButton(text='Save', pos=(r,row), size=(rs,1), parent=scrollArea.viewport(), visible=False)
        
    # App Selection handling
    def appSelectHandler(i):
        new_ui_conf = copy.deepcopy(ui_conf)  # <- this will cancel unexpected changes
        msg_lab._color = ERROR_COLOR; msg_lab._text = ""; msg_lab.update()
        choice = apps_list[i]
        extra['choice'] = choice
        
        inp_title_lab.visible=True; inp_title_lab.show(); inp_title_lab.update()
        inp_title.visible=True; inp_title.show(); inp_title.update()
        inp_descr_lab.visible=True; inp_descr_lab.show(); inp_descr_lab.update()
        inp_descr.visible=True; inp_descr.show(); inp_descr.update()
        inp_port_lab.visible=True; inp_port_lab.show(); inp_port_lab.update()
        inp_port.visible=True; inp_port.show(); inp_port.update()
        inp_img_lab.visible=True; inp_img_lab.show(); inp_img_lab.update()
        inp_img.visible=True; inp_img.show(); inp_img.update()
        inp_path_lab.visible=True; inp_path_lab.show(); inp_path_lab.update()
        inp_path.visible=True; inp_path.show(); inp_path.update()

        if choice != CREATE_NEW:
            appd = new_ui_conf[tab][choice]
            if "path" not in appd: appd['path'] = ""
            inp_title._text = appd['title']; inp_title.update()
            inp_descr._text = appd['description']; inp_descr.update()
            inp_port._text = str(appd['port']); inp_port.update()
            inp_img._text = TTkString(appd['image']); inp_img.update()
            inp_path._text = str(appd['path']); inp_path.update()
            # Show delete, cancel and save buttons
            btn_delete.show()
            btn_cancel._visible=True; btn_cancel.update()
            btn_save._visible=True; btn_save.update()
        else:  # <- create new 
            inp_title._text = ""; inp_title.update()
            inp_descr._text = ""; inp_descr.update()
            inp_port._text = ""; inp_port.update()
            inp_img._text = TTkString(""); inp_img.update()
            inp_path._text = ""; inp_path.update()
            btn_delete.hide()
            btn_cancel._visible=True; btn_cancel.update()
            btn_save._visible=True; btn_save.update()
    app_select.currentIndexChanged.connect(lambda i : appSelectHandler(i))

    # Create new handling
    def _btnSaveHandler():
        if extra['choice'] == CREATE_NEW:
            pass
    btn_save.clicked.connect(_btnSaveHandler)

    # Text input handlers
    def _processMetaInput(what, n): 
        nonlocal extra; nonlocal new_app
        choice =  extra['choice']
        # remove trailing / from path if any
        if what == 'path' and len(n) > 0 and n[0] == "/":
            n = n[1:]
        # update respective dict
        if choice != CREATE_NEW:
            if tab != "" and choice != "":
                new_ui_conf[tab][choice][what] = n
        else: new_app[what] = n
        msg_lab._color = ERROR_COLOR; msg_lab._text = ""; msg_lab.update()
    # Bind text inputs
    inp_title.textEdited.connect(lambda n: _processMetaInput('title', n))
    inp_descr.textEdited.connect(lambda n: _processMetaInput('description', n))
    inp_port.textEdited.connect(lambda n: _processMetaInput('port', n))
    inp_port.textEdited.connect(lambda n: _processMetaInput('port', n))
    inp_path.textEdited.connect(lambda n: _processMetaInput('path', n))


    # File Picker processor
    def _updImg(val):
        nonlocal extra; nonlocal new_app
        choice =  extra['choice']
        if choice != CREATE_NEW:
            new_ui_conf[tab][choice]["image"] = val
        else:
            new_app["image"] = val
        inp_img._text = TTkString(val)
        msg_lab._color = ERROR_COLOR; msg_lab._text = ""; msg_lab.update()
    def _ImageFilePickerDialog(fm):
        filePicker = ttk.TTkFileDialogPicker(pos = (3,3), size=(95,24), caption="Pick Something", path=".", fileMode=fm ,filter="All Files (*);;SVG files (*.svg);;PNG images (*.png);;JPG images (*.jpg)")
        filePicker.pathPicked.connect(lambda fi : _updImg(fi))
        ttk.TTkHelper.overlay(scrollArea, filePicker, 2, 1, True)
    # Bind Image File Picker buttons
    inp_img.clicked.connect(lambda : _ImageFilePickerDialog(ttk.TTkK.FileMode.AnyFile))


    # Delete Button processor
    def _deletelBtn(): 
        nonlocal ui_conf; nonlocal new_ui_conf; nonlocal extra; nonlocal new_app 
        # Remove the entry from the new_ui_conf
        choice =  extra['choice']
        del new_ui_conf[tab][choice]
        update_ui_conf(new_ui_conf)
        ui_conf[tab] = copy.deepcopy(new_ui_conf[tab])
        # Update the UI
        apps_list.remove(choice)
        app_select._list = apps_list; app_select.update()
        app_select.setCurrentIndex(-1)
        inp_title._text = ""; inp_title.update()
        inp_descr._text = ""; inp_descr.update()
        inp_port._text = ""; inp_port.update()
        inp_path._text = ""; inp_path.update()
        inp_img._text = TTkString(""); inp_img.update()
        refresh_from_meta()
    # Bind delete button
    btn_delete.clicked.connect(_deletelBtn)

    # Cancel Button processor
    def _cancelBtn(): 
        nonlocal ui_conf; nonlocal new_ui_conf; nonlocal extra; nonlocal new_app 
        choice =  extra['choice']
        if choice != CREATE_NEW:
            appd = ui_conf[tab][choice]
            if "path" not in appd: appd['path'] = ""
            inp_title._text = str(appd["title"]); inp_title.update()
            inp_descr._text = str(appd["description"]); inp_descr.update()
            inp_port._text = str(appd["port"]); inp_port.update()
            inp_img._text = TTkString(appd["image"]); inp_img.update()
            inp_path._text = str(appd["path"]); inp_path.update()
            new_ui_conf = copy.deepcopy(ui_conf)
        else:
            inp_title._text = ""; inp_title.update()
            inp_descr._text = ""; inp_descr.update()
            inp_port._text = ""; inp_port.update()
            inp_path._text = ""; inp_path.update()
            inp_img._text = TTkString(""); inp_img.update()
    # Bind cancel button
    btn_cancel.clicked.connect(_cancelBtn)

    # Save Button processor
    def _saveBtn(): 
        nonlocal ui_conf; nonlocal new_ui_conf; nonlocal extra; nonlocal apps_list
        choice =  extra['choice']
        if choice != CREATE_NEW:
            # checks all fields provided
            if new_ui_conf[tab][choice]['title'] == "": 
                msg_lab._color = ERROR_COLOR; msg_lab._text = "Please enter title"; msg_lab.update()
                return
            if new_ui_conf[tab][choice]['description'] == "": 
                msg_lab._color = ERROR_COLOR; msg_lab._text = "Please enter description"; msg_lab.update()
                return
            if new_ui_conf[tab][choice]['port'] == "": 
                msg_lab._color = ERROR_COLOR; msg_lab._text = "Please enter port"; msg_lab.update()
                return
            if not str(new_ui_conf[tab][choice]['port']).isnumeric():
                msg_lab._color = ERROR_COLOR; msg_lab._text = "Port must be nnumeric"; msg_lab.update()
                return
            # copy image file physically (if changed)
            if new_ui_conf[tab][choice]['image'] != ui_conf[tab][choice]['image']:
                new_img_path = copy_pageapp_image(tab, new_ui_conf[tab][choice]['image'])
                new_ui_conf[tab][choice]['image'] = new_img_path
                inp_img._text = TTkString(new_img_path); inp_img.update()
            # Make port int
            new_ui_conf[tab][choice]['port'] = int(new_ui_conf[tab][choice]['port'])
            # Save new configuration
            update_ui_conf(new_ui_conf)
            ui_conf[tab] = new_ui_conf[tab]
        else:
            # perform checks required fields
            if 'title' not in new_app or new_app['title'] == "": 
                msg_lab._color = ERROR_COLOR; msg_lab._text = "Please enter title"; msg_lab.update()
                return
            if 'description' not in new_app or new_app['description'] == "": 
                msg_lab._color = ERROR_COLOR; msg_lab._text = "Please enter description"; msg_lab.update()
                return
            if 'port' not in new_app or new_app['port'] == "": 
                msg_lab._color = ERROR_COLOR; msg_lab._text = "Please enter port"; msg_lab.update()
                return
            if not str(new_app['port']).isnumeric(): 
                msg_lab._color = ERROR_COLOR; msg_lab._text = "Port must be nnumeric"; msg_lab.update()
                return
            if 'image' not in new_app or new_app['image'] == "": 
                msg_lab._color = ERROR_COLOR; msg_lab._text = "Please choose image"; msg_lab.update()
                return
            # copy new image physically
            new_img_path = copy_pageapp_image(tab, new_app["image"])
            new_app["image"] = new_img_path
            new_app["port"] = int(new_app["port"])
            inp_img._text = TTkString(new_img_path); inp_img.update()
            # create new entry in the new_ui_conf
            newtitle = safestring(new_app['title'])
            new_ui_conf[tab][newtitle] = new_app
            update_ui_conf(new_ui_conf)
            ui_conf = copy.deepcopy(new_ui_conf)
            # Update the UI
            apps_list.append(newtitle)
            app_select._list = apps_list; app_select.update()
            app_select.setCurrentIndex(apps_list.index(newtitle))
        ui_conf[tab] = copy.deepcopy(new_ui_conf[tab])
        refresh_from_meta()
    btn_save.clicked.connect(_saveBtn)

    return scrollArea



def get_interface_widget():
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

    return wrap_widg



