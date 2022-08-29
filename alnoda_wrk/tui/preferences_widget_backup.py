import TermTk as ttk
from helper_vidgets import make_horizontal_pair


def get_preferences_widget(label_color):
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)

    l = ttk.TTkLabel(text='Font', color=label_color)
    v = ttk.TTkLineEdit(text='Roboto')
    g = make_horizontal_pair(l, v)
    wrap_widg.layout().addWidget(g)

    l = ttk.TTkLabel(text='Logo', color=label_color)
    logo_btn = ttk.TTkButton(size=(8,3),  border=0, text='File' )
    g = make_horizontal_pair(l, logo_btn)
    wrap_widg.layout().addWidget(g)

    l = ttk.TTkLabel(text='Favicon', color=label_color)
    favicon_btn = ttk.TTkButton(size=(8,3),  border=0, text='File' )
    g = make_horizontal_pair(l, favicon_btn)
    wrap_widg.layout().addWidget(g)

    l = ttk.TTkLabel(text='Light Primary', color=label_color)
    ligh_primary = ttk.TTkColorButtonPicker(pos=( 0,0), size=(8,3), border=0, color=ttk.TTkColor.bg('#88ffff'))
    g = make_horizontal_pair(l, ligh_primary)
    wrap_widg.layout().addWidget(g)

    # Buttons
    btn_widget = ttk.TTkFrame(layout= ttk.TTkGridLayout(columnMinWidth=1), border=0)
    btn_widget.setPadding(15,1,2,2)
    cancel_btn = ttk.TTkButton(text='Cancel')
    save_btn = ttk.TTkButton(text='Save')
    btn_widget.layout().addWidget(cancel_btn, 1, 0)
    btn_widget.layout().addWidget(save_btn, 1, 2)
    wrap_widg.layout().addWidget(btn_widget)

    def _showDialog(fm):
        filePicker = ttk.TTkFileDialogPicker(pos = (3,3), size=(100,25), caption="Pick Something", path=".", fileMode=fm ,filter="All Files (*);;Python Files (*.py);;Bash scripts (*.sh);;Markdown Files (*.md)")
        ttk.TTkHelper.overlay(wrap_widg, filePicker, 2, 1, True)

    logo_btn.clicked.connect(lambda : _showDialog(ttk.TTkK.FileMode.AnyFile))
    favicon_btn.clicked.connect(lambda : _showDialog(ttk.TTkK.FileMode.Directory))

    return wrap_widg