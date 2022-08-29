import sys, os, argparse, math, random

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk
from TermTk.TTkCore.color import TTkColor
from home import WrkHomeTab
from features_widget import get_features_widget
from description_widget import get_description_widget
from preferences_widget import get_preferences_widget

options = ["Home", "Features", "Description", "Preferences", "Intrerface"]
label_color = TTkColor.fg('#ebcf34')


def demoList(root= None):
    # ttk.TTkLogViewer(parent=root)
    frame = ttk.TTkFrame(parent=root, border=False)

    # Create internal window
    w = root._width; h = root._height
    mw = 140; mh = 30; mx = int((w - mw)/2); my = int((h - mh)/2)
    mainw = ttk.TTkWindow(parent=frame, size=(mw,mh), pos=(mx,my), title="Alnoda admin", border=True, layout=ttk.TTkGridLayout())

    splitter = ttk.TTkSplitter(parent=mainw, orientation=ttk.TTkK.HORIZONTAL)
    frame1 = ttk.TTkFrame(parent=splitter, border=0, layout=ttk.TTkVBoxLayout())
    frame2 = ttk.TTkFrame(parent=splitter, border=0, layout=ttk.TTkVBoxLayout())
    
    # Selection List
    listWidget = ttk.TTkList(parent=frame1, maxWidth=20, minWidth=20)
    listWidget.setPadding(1,1,1,1)

    # Home tab
    hello_widget = WrkHomeTab(border=0)
    r_widget = hello_widget
    frame2.layout().addWidget(hello_widget)

    @ttk.pyTTkSlot(str)
    def _listCallback1(label):
        nonlocal r_widget
        r_widget.hide(); r_widget.close()
        r_widget._canvas.clean()
        frame2.layout().removeWidget(r_widget); frame2._canvas.clean()
        frame2.hide()
        if label == "Home":                 r_widget = hello_widget
        elif label == "Features":           r_widget = get_features_widget(parent=frame2, label_color=label_color)
        elif label == "Description":        r_widget = get_description_widget(parent=frame2, label_color=label_color)
        elif label == "Preferences":        r_widget = get_preferences_widget(parent=frame2, label_color=label_color)
        else:                               r_widget = hello_widget
        frame2.show()
        frame2.layout().addWidget(r_widget)
        r_widget.show()
    

    # Connect the signals to the 2 slots defines
    listWidget.textClicked.connect(_listCallback1)

    # populate the lists with random entries
    for option in options:
        listWidget.addItem(f"{option}")

    return splitter





def main():
    root = ttk.TTk()
    root.setLayout(ttk.TTkGridLayout())
    demoList(root)
    root.mainloop()

if __name__ == "__main__":
    main()