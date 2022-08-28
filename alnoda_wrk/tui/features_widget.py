import TermTk as ttk

def get_features_widget(parent, label_color):
    wrap_widg = ttk.TTkFrame(parent=parent, layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)
    features_widget = ttk.TTkFrame(parent=wrap_widg, layout= ttk.TTkGridLayout(columnMinWidth=1), border=0)
    features_widget.setPadding(1,20,2,2)
    row = 1
    row +=1;  features_widget.layout().addWidget(ttk.TTkLabel(text='Workspace name', color=label_color),row,0)
    features_widget.layout().addWidget(ttk.TTkLineEdit(text='alnoda'),row,2)
    row += 1; features_widget.layout().addWidget(ttk.TTkLabel(text='Workspace version', color=label_color),row,0)
    features_widget.layout().addWidget(ttk.TTkLineEdit(text='2.2'),row,2)
    row += 1; features_widget.layout().addWidget(ttk.TTkLabel(text='Workspace author', color=label_color),row,0)
    features_widget.layout().addWidget(ttk.TTkLineEdit(text='bluxmit'),row,2)
    #
    btn_widget = ttk.TTkFrame(parent=wrap_widg, layout= ttk.TTkGridLayout(columnMinWidth=1), border=0)
    btn_widget.layout().addWidget(ttk.TTkButton(text='Cancel'),row,0)
    btn_widget.layout().addWidget(ttk.TTkButton(text='Save'),row,2)
    return wrap_widg