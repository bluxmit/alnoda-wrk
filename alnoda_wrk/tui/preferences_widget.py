import TermTk as ttk
from helper_vidgets import make_horizontal_pair


def featureScrollArea(label_color, wrap_widg):
    scrollArea = ttk.TTkScrollArea(parent=None, border=0, minHeight=22)
    l = 2; ls = 50
    r = 55; rs = 60 
    row = 0
    ttk.TTkLabel(text='Font', color=label_color, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ttk.TTkLineEdit(text='Roboto', pos=(r,row), size=(rs,1), parent=scrollArea.viewport())

    row+=2; ttk.TTkLabel(text='Logo', color=label_color, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    logo_btn = ttk.TTkButton(text='File', pos=(r,row), size=(rs,1), parent=scrollArea.viewport())
    
    row+=2; ttk.TTkLabel(text='Favicon', color=label_color, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    favicon_btn = ttk.TTkButton(text='File', pos=(r,row), size=(rs,1), parent=scrollArea.viewport())

    # l = ttk.TTkLabel(text='Logo', color=label_color)
    # logo_btn = ttk.TTkButton(size=(8,3),  border=0, text='File' )

    # l = ttk.TTkLabel(text='Favicon', color=label_color)
    # favicon_btn = ttk.TTkButton(size=(8,3),  border=0, text='File' )

    row+=2; ttk.TTkLabel(text='Primary color', color=label_color, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ligh_primary = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#88ffff'))

    # Bind buttons
    def _showDialog(fm):
        filePicker = ttk.TTkFileDialogPicker(pos = (3,3), size=(100,25), caption="Pick Something", path=".", fileMode=fm ,filter="All Files (*);;Python Files (*.py);;Bash scripts (*.sh);;Markdown Files (*.md)")
        ttk.TTkHelper.overlay(wrap_widg, filePicker, 2, 1, True)

    logo_btn.clicked.connect(lambda : _showDialog(ttk.TTkK.FileMode.AnyFile))
    favicon_btn.clicked.connect(lambda : _showDialog(ttk.TTkK.FileMode.Directory))

    return scrollArea




def get_preferences_widget(label_color):
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=True)

    # Scroll area
    scrollarea = featureScrollArea(label_color, wrap_widg)
    wrap_widg.layout().addWidget(scrollarea)

    # Buttons
    btn_widget = ttk.TTkFrame(layout= ttk.TTkGridLayout(columnMinWidth=1), border=0)
    btn_widget.setPadding(1,1,2,2)
    btn_widget.layout().addWidget(ttk.TTkButton(text='Cancel'), 1, 0)
    btn_widget.layout().addWidget(ttk.TTkButton(text='Save'), 1, 2)
    wrap_widg.layout().addWidget(btn_widget)

    return wrap_widg