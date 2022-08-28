
import sys, os, argparse, math, random

sys.path.append(os.path.join(sys.path[0],'../..'))
import TermTk as ttk

options = ["features", "settings", "applications"]


def demoList(root= None):
    # Define the main Layout
    splitter = ttk.TTkSplitter(parent=root, orientation=ttk.TTkK.HORIZONTAL)
    frame1 = ttk.TTkFrame(parent=splitter, border=0, layout=ttk.TTkVBoxLayout())
    frame3 = ttk.TTkFrame(parent=splitter, border=0, layout=ttk.TTkVBoxLayout())

    # Single Selection List
    listWidgetSingle = ttk.TTkList(parent=frame1, maxWidth=40, minWidth=10)

    # Log Viewer
    label1 = ttk.TTkLabel(parent=frame3, text="[ list1 ]",maxHeight=2)
    ttk.TTkLogViewer(parent=frame3)#, border=True)

    @ttk.pyTTkSlot(str)
    def _listCallback1(label):
        ttk.TTkLog.info(f"Clicked label1: {label}")
        label1.text = f"[ list1 ] clicked {label}"

    # Connect the signals to the 2 slots defines
    listWidgetSingle.textClicked.connect(_listCallback1)

    # populate the lists with random entries
    for option in options:
        listWidgetSingle.addItem(f"{option}")

    return splitter








def main():
    root = ttk.TTk()
    root.setLayout(ttk.TTkGridLayout())
    mainw = ttk.TTkWindow(parent=root,pos=(1,1), title="Alnoda admin", border=True, layout=ttk.TTkGridLayout())
    demoList(mainw)
    root.mainloop()

if __name__ == "__main__":
    main()