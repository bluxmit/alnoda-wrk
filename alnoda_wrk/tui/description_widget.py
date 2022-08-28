import TermTk as ttk

def get_description_widget(label_color, parent):
    # Description
    wrap_widg = ttk.TTkFrame(parent=parent, layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)
    lab_widget = ttk.TTkFrame(parent=wrap_widg, layout= ttk.TTkVBoxLayout(columnMinWidth=1), border=0, maxHeight=3)
    lab_widget.setPadding(1,1,2,2)
    lab_widget.layout().addWidget(ttk.TTkLabel(text='Edit workspace description', color=label_color))

    description_widget = ttk.TTkFrame(parent=wrap_widg, layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=1, maxHeight=20)
    description_widget.setPadding(1,1,2,2)
    document=ttk.TTkTextDocument()
    te = ttk.TTkTextEdit(document=document)
    te.setReadOnly(False)
    te.setText(ttk.TTkString("Text Edit DEMO \n adfasf afd asf af \n aasdasd adsasd asd asd \n adsasdasda a. sd asa "))
    description_widget.layout().addWidget(te)

    bt_widget = ttk.TTkFrame(parent=wrap_widg, layout=ttk.TTkGridLayout(columnMinWidth=1), border=0)
    bt_widget.setPadding(1,0,0,0)
    bt_widget.layout().addWidget(ttk.TTkButton(text='Cancel'),1,0)
    bt_widget.layout().addWidget(ttk.TTkButton(text='Save'),1,2)
    return wrap_widg