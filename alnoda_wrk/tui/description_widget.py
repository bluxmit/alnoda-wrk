import TermTk as ttk
import copy
from .gvars import *
from ..fileops import read_meta
from ..meta_about import update_workspace_description

def get_description_widget():
    # Get actual values
    meta = read_meta()
    new_meta = copy.deepcopy(meta)

    # Description
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)
    wrap_widg.setPadding(1,1,2,2)

    # Edit label
    lab_widget = ttk.TTkFrame(layout= ttk.TTkVBoxLayout(columnMinWidth=1), border=0, maxHeight=2)
    lab_widget.setPadding(0,1,0,0)
    l = ttk.TTkLabel(text='Edit workspace description (Markdown)', color=LABEL_COLOR)
    lab_widget.layout().addWidget(l)
    wrap_widg.layout().addWidget(lab_widget)

    # Description
    description_widget = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=1, minHeight=20, maxHeight=21)
    description_widget.setPadding(1,1,2,2)
    document=ttk.TTkTextDocument()
    description_edit = ttk.TTkTextEdit(document=document)
    description_edit.setReadOnly(False)
    description_edit.setText(ttk.TTkString(str(meta['description'])))
    description_widget.layout().addWidget(description_edit)
    wrap_widg.layout().addWidget(description_widget)

    # Text Input processor
    def _processDescrUpdate(): 
        new_meta['description'] = "\n".join([l._text for l in document._dataLines])
    # Bind Text Input
    document.contentsChange.connect(lambda n, y, z : _processDescrUpdate())

    # Buttons
    btn_widget = ttk.TTkFrame(layout = ttk.TTkGridLayout(columnMinWidth=1), border=0)
    btn_widget.setPadding(1,1,2,2)
    btn_cancel = ttk.TTkButton(text = 'Cancel')
    btn_save = ttk.TTkButton(text = 'Save')
    btn_widget.layout().addWidget(btn_cancel, 1, 0)
    btn_widget.layout().addWidget(btn_save, 1, 2)
    wrap_widg.layout().addWidget(btn_widget)

    # Button processors
    def _cancelBtn():
        nonlocal meta; nonlocal new_meta
        description_edit.setText(ttk.TTkString(str(meta['description'])))
        new_meta = copy.deepcopy(meta)
    def _savelBtn(): 
        nonlocal meta; nonlocal new_meta
        update_workspace_description(new_meta['description'])
        meta = copy.deepcopy(new_meta)
    # Connect buttons
    btn_cancel.clicked.connect(lambda : _cancelBtn())    
    btn_save.clicked.connect(lambda : _savelBtn())

    return wrap_widg