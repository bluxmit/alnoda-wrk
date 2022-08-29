import TermTk as ttk
from helper_vidgets import make_horizontal_pair
from gvars import *


def get_features_widget():
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)

    l = ttk.TTkLabel(text='Workspace name', color=LABEL_COLOR)
    v = ttk.TTkLineEdit(text='alnoda')
    g = make_horizontal_pair(l, v)
    wrap_widg.layout().addWidget(g)

    l = ttk.TTkLabel(text='Workspace version', color=LABEL_COLOR)
    v = ttk.TTkLineEdit(text='4.0')
    g = make_horizontal_pair(l, v)
    wrap_widg.layout().addWidget(g)

    l = ttk.TTkLabel(text='Workspace author', color=LABEL_COLOR)
    v = ttk.TTkLineEdit(text='bluxmit')
    g = make_horizontal_pair(l, v)
    wrap_widg.layout().addWidget(g)

    l = ttk.TTkLabel(text='Documentation link', color=LABEL_COLOR)
    v = ttk.TTkLineEdit(text='https://docs.alnoda.org/')
    g = make_horizontal_pair(l, v)
    wrap_widg.layout().addWidget(g)
    
    # Buttons
    btn_widget = ttk.TTkFrame(layout= ttk.TTkGridLayout(columnMinWidth=1), border=0)
    btn_widget.setPadding(16,1,2,2)
    btn_widget.layout().addWidget(ttk.TTkButton(text='Cancel'), 1, 0)
    btn_widget.layout().addWidget(ttk.TTkButton(text='Save'), 1, 2)
    wrap_widg.layout().addWidget(btn_widget)

    return wrap_widg