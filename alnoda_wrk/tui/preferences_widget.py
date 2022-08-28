import TermTk as ttk


def get_preferences_widget(parent, label_color):
    wrap_widg = ttk.TTkFrame(parent=parent, layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)
    preferences_widget = ttk.TTkFrame(parent=wrap_widg, layout= ttk.TTkGridLayout(columnMinWidth=1), border=0)
    preferences_widget.setPadding(1,20,2,2)
    row = 1
    # Font
    row +=1;  preferences_widget.layout().addWidget(ttk.TTkLabel(text='Font', color=label_color),row,0)
    preferences_widget.layout().addWidget(ttk.TTkLineEdit(text='Roboto'),row,2)
    # Logo file
    row += 1; preferences_widget.layout().addWidget(ttk.TTkLabel(text='Logo', color=label_color),row,0)
    logo_btn = ttk.TTkButton(size=(8,3),  border=0, text='File' )
    preferences_widget.layout().addWidget(logo_btn, row,2)
    # Favicon file
    row += 1; preferences_widget.layout().addWidget(ttk.TTkLabel(text='Favicon', color=label_color),row,0)
    favicon_btn = ttk.TTkButton(size=(8,3),  border=0, text='File' )
    preferences_widget.layout().addWidget(favicon_btn, row,2)
    #
    btn_widget = ttk.TTkFrame(parent=wrap_widg, layout= ttk.TTkGridLayout(columnMinWidth=1), border=0)
    btn_widget.layout().addWidget(ttk.TTkButton(text='Cancel'),row,0)
    btn_widget.layout().addWidget(ttk.TTkButton(text='Save'),row,2)

    label = ttk.TTkLabel(parent=parent, pos=(1,5), size=(30,1), text="...")
    def _showDialog(fm):
        filePicker = ttk.TTkFileDialogPicker(pos = (3,3), size=(100,25), caption="Pick Something", path=".", fileMode=fm ,filter="All Files (*);;Python Files (*.py);;Bash scripts (*.sh);;Markdown Files (*.md)")
        filePicker.pathPicked.connect(label.setText)
        ttk.TTkHelper.overlay(parent, filePicker, 2, 1, True)

    logo_btn.clicked.connect(lambda : _showDialog(ttk.TTkK.FileMode.AnyFile))
    favicon_btn.clicked.connect(lambda : _showDialog(ttk.TTkK.FileMode.Directory))
    return wrap_widg