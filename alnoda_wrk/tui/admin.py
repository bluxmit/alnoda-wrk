import sys, os, argparse, math, random

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk
from TermTk.TTkCore.color import TTkColor
from home import WrkHomeTab

options = ["home", "features", "settings", "applications", "logs"]




def demoList(root= None):
    frame = ttk.TTkFrame(parent=root, border=False)

    # Create internal window
    w = root._width; h = root._height
    mw = 140; mh = 50; mx = int((w - mw)/2); my = int((h - mh)/2)
    mainw = ttk.TTkWindow(parent=frame, size=(mw,mh), pos=(mx,my), title="Alnoda admin", border=True, layout=ttk.TTkGridLayout())


    splitter = ttk.TTkSplitter(parent=mainw, orientation=ttk.TTkK.HORIZONTAL)
    frame1 = ttk.TTkFrame(parent=splitter, border=0, layout=ttk.TTkVBoxLayout())
    frame3 = ttk.TTkFrame(parent=splitter, border=0, layout=ttk.TTkVBoxLayout())

    # Selection List
    listWidget = ttk.TTkList(parent=frame1, maxWidth=20, minWidth=20)

    # Home tab
    hello_widget = WrkHomeTab(border=0)
    # hello_widget = WrkHomeTab(border=1)
    
    # Features
    # features_widget = ttk.TTkFrame(parent=splitter, border=0, layout=ttk.TTkVBoxLayout())
    # ttk.TTkInput(parent=features_widget)
    # frame3.addWidget(r_widget)

    # Define initial right widget
    label1 = ttk.TTkLabel(parent=frame3, text="[ list1 ]",maxHeight=2)
    r_widget = hello_widget
    frame3.layout().addWidget(r_widget)

    @ttk.pyTTkSlot(str)
    def _listCallback1(label):
        nonlocal r_widget
        ttk.TTkLog.info(f"Clicked label1: {label}")
        ttk.TTkLog.info(f"root._width  {root._width}")
        ttk.TTkLog.info(f"root._height  {root._height}")
        ttk.TTkLog.info(f"mx  {mx}")
        ttk.TTkLog.info(f"my  {my}")
        ttk.TTkLog.info(f"hello_widget_width  {hello_widget._width}")
        ttk.TTkLog.info(f"hello_widget_height  {hello_widget._height}")
        # ttk.TTkLog.info(f"ttk.TTkCore.constant.TTkConstant.Alignment {ttk.TTkCore.constant.TTkConstant.Alignment}")
        # ttk.TTkLog.info(f"ttk.TTkCore.constant.TTkConstant.CENTER {ttk.TTkCore.constant.TTkConstant.CENTER}")
        # ttk.TTkLog.info(f"ttk.TTkCore.constant.TTkConstant.CENTER_ALIGN {ttk.TTkCore.constant.TTkConstant.CENTER_ALIGN}")
        label1.text = f"[ list1 ] clicked {label}"
        frame3.layout().removeWidget(r_widget)
        if label == "logs": 
            r_widget = ttk.TTkLogViewer()
        elif label == "home":
            r_widget = hello_widget
        frame3.layout().addWidget(r_widget)


        

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