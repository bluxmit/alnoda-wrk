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
    new_meta = copy.deepcopy(meta)
    
    # Generate widgets
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)

    l = ttk.TTkLabel(text="Workspace name", color=LABEL_COLOR)
    name_inp = ttk.TTkLineEdit(text=str(meta['name']))
    g = make_horizontal_pair(l, name_inp)
    wrap_widg.layout().addWidget(g)

    l = ttk.TTkLabel(text="Workspace version", color=LABEL_COLOR)
    version_inp = ttk.TTkLineEdit(text=str(meta['version']))
    g = make_horizontal_pair(l, version_inp)
    wrap_widg.layout().addWidget(g)

    l = ttk.TTkLabel(text="Workspace author", color=LABEL_COLOR)
    author_inp = ttk.TTkLineEdit(text=str(meta['author']))
    g = make_horizontal_pair(l, author_inp)
    wrap_widg.layout().addWidget(g)

    l = ttk.TTkLabel(text="Workspace documentation", color=LABEL_COLOR)
    docs_inp = ttk.TTkLineEdit(text=str(meta['docs']))
    g = make_horizontal_pair(l, docs_inp)
    wrap_widg.layout().addWidget(g)

    l = ttk.TTkLabel(text="Tags", color=LABEL_COLOR)
    tags_inp = ttk.TTkLineEdit(text=str(meta['tags']))
    g = make_horizontal_pair(l, tags_inp)
    wrap_widg.layout().addWidget(g)

    # Text Input processor
    def _processMetaInput(what, n): new_meta[what] = n
    # Bind Text Input
    name_inp.textEdited.connect(lambda n: _processMetaInput('name', n))
    version_inp.textEdited.connect(lambda n: _processMetaInput('version', n))
    author_inp.textEdited.connect(lambda n: _processMetaInput('author', n))
    docs_inp.textEdited.connect(lambda n: _processMetaInput('docs', n))
    tags_inp.textEdited.connect(lambda n: _processMetaInput('tags', n))
    
    # Buttons
    btn_widget = ttk.TTkFrame(layout= ttk.TTkGridLayout(columnMinWidth=1), border=0)
    btn_widget.setPadding(14,1,2,2)
    btn_cancel = ttk.TTkButton(text='Cancel')
    btn_save = ttk.TTkButton(text='Save')
    btn_widget.layout().addWidget(btn_cancel, 1, 0)
    btn_widget.layout().addWidget(btn_save, 1, 2)
    wrap_widg.layout().addWidget(btn_widget)

    # Button processors
    def _cancelBtn():
        nonlocal meta; nonlocal new_meta
        name_inp._text = str(meta['name']); name_inp.update()
        version_inp._text = str(meta['version']); version_inp.update()
        author_inp._text = str(meta['author']); author_inp.update()
        docs_inp._text = str(meta['docs']); docs_inp.update()
        new_meta = copy.deepcopy(meta)
    def _savelBtn():
        nonlocal meta; nonlocal new_meta
        update_meta(name=new_meta['name'], version=new_meta['version'], author=new_meta['author'], docs=new_meta['docs'], tags=new_meta['tags'])
        refresh_from_meta()
        meta = copy.deepcopy(new_meta)
    # Connect buttons
    btn_cancel.clicked.connect(lambda : _cancelBtn())    
    btn_save.clicked.connect(lambda : _savelBtn())
    return wrap_widg