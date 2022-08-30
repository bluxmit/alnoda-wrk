import TermTk as ttk
from .helper_vidgets import make_horizontal_pair
from .gvars import *


def get_interface_widget():
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)
    tabArea = ttk.TTkTabWidget(border=True, minHeight=23)
    wrap_widg.layout().addWidget(tabArea)

    tab1_widg = ttk.TTkFrame(border=0, visible=True)
    tab1 = tabArea.addTab(tab1_widg,  "Home")
    
    tab2_widg = ttk.TTkFrame(border=0, visible=True)
    tab2 = tabArea.addTab(tab2_widg,  "My Apps")

    # Buttons
    btn_widget = ttk.TTkFrame(layout= ttk.TTkGridLayout(columnMinWidth=1), border=0)
    btn_widget.setPadding(1,1,2,2)
    btn_widget.layout().addWidget(ttk.TTkButton(text='Cancel'), 1, 0)
    btn_widget.layout().addWidget(ttk.TTkButton(text='Save'), 1, 2)
    wrap_widg.layout().addWidget(btn_widget)

    return wrap_widg



