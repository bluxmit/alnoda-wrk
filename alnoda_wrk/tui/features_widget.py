import TermTk as ttk
from helper_vidgets import make_horizontal_pair


def get_features_widget(label_color):
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)

    l = ttk.TTkLabel(text='Workspace name', color=label_color)
    v = ttk.TTkLineEdit(text='alnoda')
    g = make_horizontal_pair(l, v)
    wrap_widg.layout().addWidget(g)

    l = ttk.TTkLabel(text='Workspace version', color=label_color)
    v = ttk.TTkLineEdit(text='4.0')
    g = make_horizontal_pair(l, v)
    wrap_widg.layout().addWidget(g)

    l = ttk.TTkLabel(text='Workspace author', color=label_color)
    v = ttk.TTkLineEdit(text='bluxmit')
    g = make_horizontal_pair(l, v)
    wrap_widg.layout().addWidget(g)
    
    # Buttons
    btn_widget = ttk.TTkFrame(layout= ttk.TTkGridLayout(columnMinWidth=1), border=0)
    btn_widget.setPadding(18,1,2,2)
    btn_widget.layout().addWidget(ttk.TTkButton(text='Cancel'), 1, 0)
    btn_widget.layout().addWidget(ttk.TTkButton(text='Save'), 1, 2)
    wrap_widg.layout().addWidget(btn_widget)

    return wrap_widg