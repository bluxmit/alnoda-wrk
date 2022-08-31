import copy
import TermTk as ttk
from TermTk.TTkCore.string import TTkString
from .helper_vidgets import make_horizontal_pair
from .gvars import *
from ..fileops import read_ui_conf, update_ui_conf
from ..globals import *


def find_title_in_dict(dic, title):
    """
    """
    for k,v in dic.items():
        if v['title'] == title: 
            return v
    # if not found
    app_name = safestring(title)
    new = {'title': "", 'description': "", 'port': "", 'image': ""}
    dic[app_name] = new
    return new


def get_tab_widgets(tab, ui_conf):
    """Create widgets for the specific tab"""
    tabdata = copy.deepcopy(ui_conf[tab])
    new_tabdata = copy.deepcopy(tabdata)
    apps_list = [e['title'] for e in tabdata.values()]
    apps_list.append("CREATE NEW")
    extra = {'choice': ""}

    scrollArea = ttk.TTkScrollArea(parent=None, border=0, minHeight=22)
    scrollArea.setPadding(0,0,0,2)
    l = 2; ls = 50
    r = 55; rs = 60 
    row = 1
    debt = ttk.TTkLabel(text='Chose app', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    app_select = ttk.TTkComboBox(list=apps_list, pos=(r,row), size=(rs,1))
    scrollArea.viewport().addWidget(app_select)

    row+=2; ttk.TTkLabel(text='Title', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    inp_title = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1))
    scrollArea.viewport().addWidget(inp_title)

    row+=2; ttk.TTkLabel(text='Description', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    inp_descr = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1))
    scrollArea.viewport().addWidget(inp_descr)

    row+=2; ttk.TTkLabel(text='Port (range 8021-8040)', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    inp_port = ttk.TTkLineEdit(text="", pos=(r,row), size=(rs,1))
    scrollArea.viewport().addWidget(inp_port)

    row+=2; ttk.TTkLabel(text='Image', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    inp_img = ttk.TTkButton(text="", pos=(r,row), size=(rs,1), parent=scrollArea.viewport())
    scrollArea.viewport().addWidget(inp_descr)

    # Buttons
    row+=8; btn_delete = ttk.TTkButton(text='Delete', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=False)
    btn_delete.setBorderColor(TTkColor.fg('#f20e0a'))
    row+=4; btn_cancel = ttk.TTkButton(text='Cancel', pos=(l,row), size=(ls,1), parent=scrollArea.viewport(), visible=False)
    btn_save = ttk.TTkButton(text='Save', pos=(r,row), size=(rs,1), parent=scrollArea.viewport(), visible=False)
        
    # App Selection handling
    def appSelectHandler(i):
        new_tabdata = copy.deepcopy(tabdata)  # <- this will cancel unexpected changes
        try:    # <- modify existing apps
            sel = apps_list[i]
            extra['choice'] = sel
            appd = find_title_in_dict(tabdata, sel)
            inp_title._text = appd['title']; inp_title.update()
            inp_descr._text = appd['description']; inp_descr.update()
            inp_port._text = str(appd['port']); inp_port.update()
            inp_img._text = TTkString(appd['image']); inp_img.update()
            # Show delete, cancel and save buttons
            btn_delete._visible=True; btn_delete.update()
            btn_cancel._visible=True; btn_cancel.update()
            btn_save._visible=True; btn_save.update()
        except:  # <- create new 
            inp_title._text = ""; inp_title.update()
            inp_descr._text = ""; inp_descr.update()
            inp_port._text = ""; inp_port.update()
            inp_img._text = TTkString(""); inp_img.update()
            btn_delete.hide(); btn_delete.update()
            btn_cancel._visible=True; btn_cancel.update()
            btn_save._visible=True; btn_save.update()
    app_select.currentIndexChanged.connect(lambda i : appSelectHandler(i))

    # Create new handling
    def _btnSaveHandler():
        if extra['choice'] == "CREATE NEW":
            pass
    btn_save.clicked.connect(_btnSaveHandler)

    # Text input handlers
    def _processMetaInput(what, n): 
        app =  extra['choice']
        d = find_title_in_dict(new_tabdata, app)
        d[what] = n
    # Bind text inputs
    inp_title.textEdited.connect(lambda n: _processMetaInput('title', n))
    inp_descr.textEdited.connect(lambda n: _processMetaInput('description', n))
    inp_port.textEdited.connect(lambda n: _processMetaInput('port', n))

    # File Picker processor
    def _updImg(val):
        app =  extra['choice']
        d = find_title_in_dict(new_tabdata, app)
        d["image"] = val
        inp_img._text = TTkString(val)

    def _ImageFilePickerDialog(fm):
        filePicker = ttk.TTkFileDialogPicker(pos = (3,3), size=(95,24), caption="Pick Something", path=".", fileMode=fm ,filter="All Files (*);;SVG files (*.svg);;PNG images (*.png);;JPG images (*.jpg)")
        filePicker.pathPicked.connect(lambda fi : _updImg(fi))
        ttk.TTkHelper.overlay(scrollArea, filePicker, 2, 1, True)
        
    # Bind Image File Picker buttons
    inp_img.clicked.connect(lambda : _ImageFilePickerDialog(ttk.TTkK.FileMode.AnyFile))

    # Cancel Button processor
    def _cancelBtn(): 
        nonlocal tabdata; nonlocal new_tabdata; nonlocal extra 
        sel = extra['choice']
        d = find_title_in_dict(tabdata, extra['choice'])
        inp_title._text = d["title"]; inp_title.update()
        inp_descr._text = d["description"]; inp_descr.update()
        inp_port._text = str(d["port"]); inp_port.update()
        inp_img._text = TTkString(d["image"]); inp_img.update()
        new_tabdata = copy.deepcopy(tabdata)
    # Bind cancel button
    btn_cancel.clicked.connect(_cancelBtn)

    # Save Button processor
    def _saveBtn(): 
        nonlocal ui_conf; nonlocal tabdata; nonlocal new_tabdata; nonlocal extra 
        ui_conf[tab] = new_tabdata
        # debt._text = ">> "+ui_conf[tab]['FILEBROWSER']['title']; debt.update()
        update_ui_conf(ui_conf)
        tabdata = copy.deepcopy(new_tabdata)
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

    HomeScrollArea = get_tab_widgets("my_apps", ui_conf)
    tabArea.addTab(HomeScrollArea,  "My Apps")


    return wrap_widg



