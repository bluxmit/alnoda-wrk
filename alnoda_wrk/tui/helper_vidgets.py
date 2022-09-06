import os
import TermTk as ttk
from TermTk import TTkFrame, TTkWindow
from TermTk import TTkColor


def make_horizontal_pair(a, b):
    pf = ttk.TTkFrame(layout= ttk.TTkGridLayout(columnMinWidth=1), border=0)
    pf.layout().addWidget(a, 1, 0)
    pf.layout().addWidget(b, 1, 2)
    pf.setPadding(1,0,2,2)
    return pf


def get_file_viewer(file_, wrap_widg):
    content = "Nothing"
    with open(file_) as f:
        content = ttk.TTkString() + f.read() 
    sourceWin = ttk.TTkWindow(pos = (3,-2), size=(110,32), title=file_, layout=ttk.TTkGridLayout())
    texEdit = ttk.TTkTextEdit(parent=sourceWin)
    texEdit.setText(content)
    ttk.TTkHelper.overlay(wrap_widg, sourceWin, 2, 2)
    return sourceWin
