import TermTk as ttk
from gvars import *


def featureScrollArea(wrap_widg):
    scrollArea = ttk.TTkScrollArea(parent=None, border=0, minHeight=22)
    l = 2; ls = 50
    r = 55; rs = 60 
    row = 0
    ttk.TTkLabel(text='Font', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ttk.TTkLineEdit(text='Roboto', pos=(r,row), size=(rs,1), parent=scrollArea.viewport())

    row+=2; ttk.TTkLabel(text='Logo', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    logo_btn = ttk.TTkButton(text='File', pos=(r,row), size=(rs,1), parent=scrollArea.viewport())
    
    row+=2; ttk.TTkLabel(text='Favicon', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    favicon_btn = ttk.TTkButton(text='File', pos=(r,row), size=(rs,1), parent=scrollArea.viewport())

    # Light theme colors
    row+=2; ttk.TTkLabel(text='LIGHT THEME COLORS', color=SECTION_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    row+=2; ttk.TTkLabel(text='Primary', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ligh_primary = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#2A2D2E'))
    row+=2; ttk.TTkLabel(text='Accent', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ligh_accent = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#E77260'))
    row+=2; ttk.TTkLabel(text='Background', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ligh_background = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#E9EAE6'))
    row+=2; ttk.TTkLabel(text='Text', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ligh_text = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#1C1C1C'))
    row+=2; ttk.TTkLabel(text='Title', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ligh_title = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#E77260'))
    row+=2; ttk.TTkLabel(text='Subtitle', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ligh_subtitle = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#E77260'))
    row+=2; ttk.TTkLabel(text='Code', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ligh_code = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#4d4c4c'))
    row+=2; ttk.TTkLabel(text='Code background', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ligh_code_background = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#D2D2D2'))
    # show how to get the color:
    row+=2; debug_label = ttk.TTkLabel(text=f'DEBUG: ligh_code_background: {ligh_code_background.color().getHex("_fg")}', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    
    # dark theme colors
    row+=2; ttk.TTkLabel(text='DARK THEME COLORS', color=SECTION_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    row+=2; ttk.TTkLabel(text='Primary', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    dark_primary = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#3C3C3C'))
    row+=2; ttk.TTkLabel(text='Accent', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    dark_accent = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#E77260'))
    row+=2; ttk.TTkLabel(text='Background', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    dark_background = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#1E1E1E'))
    row+=2; ttk.TTkLabel(text='Text', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    dark_text = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#9CDCFE'))
    row+=2; ttk.TTkLabel(text='Title', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    dark_title = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#9CDCFE'))
    row+=2; ttk.TTkLabel(text='Subtitle', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    dark_subtitle = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#9CDCFE'))
    row+=2; ttk.TTkLabel(text='Code', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    dark_code = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#2e2b2b'))
    row+=2; ttk.TTkLabel(text='Code background', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    dark_code_background = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#ced6d6'))
    
    # common colors
    row+=2; ttk.TTkLabel(text='COMMON COLORS', color=SECTION_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    row+=2; ttk.TTkLabel(text='Header text', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    header_color = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#FFFFFF'))
    row+=2; ttk.TTkLabel(text='Navigation', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    nav_color = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.bg('#eab676'))

    # Color processor
    def _processColor(col, theme, which):
        new_color = col.getHex("_fg")
        test_message = f"new {theme} {which} - {new_color}"
        debug_label.text=test_message
    # Bind Color pickers
    ligh_code_background.colorSelected.connect(lambda col: _processColor(col, "light", "code-background"))

    return scrollArea




def get_preferences_widget():
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=True)

    # Scroll area
    scrollarea = featureScrollArea(wrap_widg)
    wrap_widg.layout().addWidget(scrollarea)

    # Buttons
    btn_widget = ttk.TTkFrame(layout= ttk.TTkGridLayout(columnMinWidth=1), border=0)
    btn_widget.setPadding(1,1,2,2)
    btn_widget.layout().addWidget(ttk.TTkButton(text='Cancel'), 1, 0)
    btn_widget.layout().addWidget(ttk.TTkButton(text='Save'), 1, 2)
    wrap_widg.layout().addWidget(btn_widget)

    return wrap_widg