import TermTk as ttk
from TermTk.TTkCore.string import TTkString

from .cheatsheet_widget import get_cheatsheet_widget
from .links_widget import get_links_widget



def get_my_notes_widget():
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)
    tabArea = ttk.TTkTabWidget(minHeight=15, border=True)
    wrap_widg.layout().addWidget(tabArea)

    # Create tabs
    LinksScrollArea = get_links_widget()
    tabArea.addTab(LinksScrollArea,  "Links")
    
    CheatsheetScrollArea = get_cheatsheet_widget()
    tabArea.addTab(CheatsheetScrollArea,  "Cheatsheet")

    return wrap_widg