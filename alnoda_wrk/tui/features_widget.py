import TermTk as ttk
import copy
from .helper_vidgets import make_horizontal_pair
from .gvars import *
from ..fileops import read_meta
from ..ui_builder import get_docs_url
from ..meta_about import update_meta, refresh_from_meta

def get_features_widget():
    # Get actual values
    meta = read_meta()
    docs_url = get_docs_url()
    new_meta = copy.deepcopy(meta)
    new_docs_url = docs_url
    
    # Generate widgets
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)

    l = ttk.TTkLabel(text="Workspace name", color=LABEL_COLOR)
    name_inp = ttk.TTkLineEdit(text=meta['name'])
    g = make_horizontal_pair(l, name_inp)
    wrap_widg.layout().addWidget(g)

    l = ttk.TTkLabel(text="Workspace version", color=LABEL_COLOR)
    version_inp = ttk.TTkLineEdit(text=meta['version'])
    g = make_horizontal_pair(l, version_inp)
    wrap_widg.layout().addWidget(g)

    l = ttk.TTkLabel(text="Workspace author", color=LABEL_COLOR)
    author_inp = ttk.TTkLineEdit(text=meta['author'])
    g = make_horizontal_pair(l, author_inp)
    wrap_widg.layout().addWidget(g)

    l = ttk.TTkLabel(text="Workspace documentation", color=LABEL_COLOR)
    docs_inp = ttk.TTkLineEdit(text=docs_url)
    g = make_horizontal_pair(l, docs_inp)
    wrap_widg.layout().addWidget(g)

    # Text Input processor
    def _processMetaInput(what, n): new_meta[what] = n
    def _docsInp(n): new_docs_url = n
    # Bind Text Input
    name_inp.textEdited.connect(lambda n: _processMetaInput('name', n))
    version_inp.textEdited.connect(lambda n: _processMetaInput('version', n))
    author_inp.textEdited.connect(lambda n: _processMetaInput('author', n))
    docs_inp.textEdited.connect(lambda n: _docsInp(n))
    
    # Buttons
    btn_widget = ttk.TTkFrame(layout= ttk.TTkGridLayout(columnMinWidth=1), border=0)
    btn_widget.setPadding(16,1,2,2)
    btn_cancel = ttk.TTkButton(text='Cancel')
    btn_save = ttk.TTkButton(text='Save')
    btn_widget.layout().addWidget(btn_cancel, 1, 0)
    btn_widget.layout().addWidget(btn_save, 1, 2)
    wrap_widg.layout().addWidget(btn_widget)

    # Button processors
    def _cancelBtn():
        name_inp._text = meta['name']; name_inp.update()
        version_inp._text = meta['version']; version_inp.update()
        author_inp._text = meta['author']; author_inp.update()
        docs_inp._text = docs_url; docs_inp.update()
        new_meta = copy.deepcopy(meta)
        new_docs_url = docs_url
    def _savelBtn():
        update_meta(name=new_meta['name'], version=new_meta['version'], author=new_meta['author'])
        refresh_from_meta()
    # Connect buttons
    btn_cancel.clicked.connect(lambda : _cancelBtn())    
    btn_save.clicked.connect(lambda : _savelBtn())
    return wrap_widg