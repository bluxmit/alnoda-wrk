import TermTk as ttk
from gvars import *


def get_description_widget():
    # Description
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)
    wrap_widg.setPadding(1,1,2,2)

    # Edit label
    lab_widget = ttk.TTkFrame(layout= ttk.TTkVBoxLayout(columnMinWidth=1), border=0, maxHeight=2)
    lab_widget.setPadding(0,1,0,0)
    lab_widget.layout().addWidget(ttk.TTkLabel(text='Edit workspace description', color=LABEL_COLOR))
    wrap_widg.layout().addWidget(lab_widget)

    # Description
    description_widget = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=1, minHeight=20, maxHeight=21)
    description_widget.setPadding(1,1,2,2)
    document=ttk.TTkTextDocument()
    te = ttk.TTkTextEdit(document=document)
    te.setReadOnly(False)
    te.setText(ttk.TTkString("Text Edit DEMO \n adfasf afd asf af \n aasdasd adsasd asd asd \n adsasdasda a. sd asa "))
    description_widget.layout().addWidget(te)
    wrap_widg.layout().addWidget(description_widget)

    # Buttons
    btn_widget = ttk.TTkFrame(layout= ttk.TTkGridLayout(columnMinWidth=1), border=0)
    btn_widget.setPadding(1,1,0, 0)
    cancel_btn = ttk.TTkButton(text='Cancel')
    save_btn = ttk.TTkButton(text='Save')
    btn_widget.layout().addWidget(cancel_btn, 1, 0)
    btn_widget.layout().addWidget(save_btn, 1, 2)
    wrap_widg.layout().addWidget(btn_widget)

    return wrap_widg