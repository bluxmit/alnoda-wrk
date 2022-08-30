import TermTk as ttk
from TermTk.TTkCore.signal import pyTTkSignal
import copy
from .gvars import *
from ..fileops import read_styles_scss, write_styles_scss


def get_preferences_widget():
    # Get existing styles 
    d_styles = read_styles_scss()
    new_d_styles = copy.deepcopy(d_styles)

    # Generate widgets
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=True)
    scrollArea = ttk.TTkScrollArea(parent=None, border=0, minHeight=22)
    wrap_widg.layout().addWidget(scrollArea)
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
    ligh_primary = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['light']['primary']))
    row+=2; ttk.TTkLabel(text='Accent', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ligh_accent = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['light']['accent']))
    row+=2; ttk.TTkLabel(text='Background', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ligh_background = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['light']['background']))
    row+=2; ttk.TTkLabel(text='Text', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ligh_text = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['light']['text']))
    row+=2; ttk.TTkLabel(text='Title', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ligh_title = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['light']['title']))
    row+=2; ttk.TTkLabel(text='Subtitle', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ligh_subtitle = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['light']['subtitle']))
    row+=2; ttk.TTkLabel(text='Code', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ligh_code = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['light']['code_text']))
    row+=2; ttk.TTkLabel(text='Code background', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    ligh_code_background = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['light']['code_background']))
    
    # dark theme colors
    row+=2; ttk.TTkLabel(text='DARK THEME COLORS', color=SECTION_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    row+=2; ttk.TTkLabel(text='Primary', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    dark_primary = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['dark']['primary']))
    row+=2; ttk.TTkLabel(text='Accent', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    dark_accent = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['dark']['accent']))
    row+=2; ttk.TTkLabel(text='Background', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    dark_background = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['dark']['background']))
    row+=2; ttk.TTkLabel(text='Text', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    dark_text = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['dark']['text']))
    row+=2; ttk.TTkLabel(text='Title', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    dark_title = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['dark']['title']))
    row+=2; ttk.TTkLabel(text='Subtitle', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    dark_subtitle = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['dark']['subtitle']))
    row+=2; ttk.TTkLabel(text='Code', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    dark_code = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['dark']['code_text']))
    row+=2; ttk.TTkLabel(text='Code background', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    dark_code_background = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['dark']['code_background']))
    
    # common colors
    row+=2; ttk.TTkLabel(text='COMMON COLORS', color=SECTION_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    row+=2; ttk.TTkLabel(text='Header text', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    header_color = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['common_colors']['header']))
    row+=2; ttk.TTkLabel(text='Navigation', color=LABEL_COLOR, pos=(l,row), size=(ls,1), parent=scrollArea.viewport())
    nav_color = ttk.TTkColorButtonPicker(pos=(r,row), size=(rs,1), border=0, parent=scrollArea.viewport(), color=ttk.TTkColor.fg(d_styles['common_colors']['nav']))

    # Color processor
    def _processColor(col, theme, which): new_d_styles[theme][which] = col.getHex("_fg")
    def _processCommonColor(col, which): new_d_styles["common_colors"][which] = col.getHex("_fg")
    # Bind Color pickers
    ligh_primary.colorSelected.connect(lambda col: _processColor(col, "light", "primary"))
    ligh_accent.colorSelected.connect(lambda col: _processColor(col, "light", "accent"))
    ligh_background.colorSelected.connect(lambda col: _processColor(col, "light", "background"))
    ligh_text.colorSelected.connect(lambda col: _processColor(col, "light", "text"))
    ligh_title.colorSelected.connect(lambda col: _processColor(col, "light", "title"))
    ligh_subtitle.colorSelected.connect(lambda col: _processColor(col, "light", "subtitle"))
    ligh_code.colorSelected.connect(lambda col: _processColor(col, "light", "code_text"))
    ligh_code_background.colorSelected.connect(lambda col: _processColor(col, "light", "code_background"))
    dark_primary.colorSelected.connect(lambda col: _processColor(col, "dark", "primary"))
    dark_accent.colorSelected.connect(lambda col: _processColor(col, "dark", "accent"))
    dark_background.colorSelected.connect(lambda col: _processColor(col, "dark", "background"))
    dark_text.colorSelected.connect(lambda col: _processColor(col, "dark", "text"))
    dark_title.colorSelected.connect(lambda col: _processColor(col, "dark", "title"))
    dark_subtitle.colorSelected.connect(lambda col: _processColor(col, "dark", "subtitle"))
    dark_code.colorSelected.connect(lambda col: _processColor(col, "dark", "code_text"))
    dark_code_background.colorSelected.connect(lambda col: _processColor(col, "dark", "code_background"))
    header_color.colorSelected.connect(lambda col: _processCommonColor(col, "header"))
    nav_color.colorSelected.connect(lambda col: _processCommonColor(col, "nav"))

    # File Picker processor
    def _FilePickerDialog(fm):
        filePicker = ttk.TTkFileDialogPicker(pos = (3,3), size=(95,24), caption="Pick Something", path=".", fileMode=fm ,filter="All Files (*);;Python Files (*.py);;Bash scripts (*.sh);;Markdown Files (*.md)")
        filePicker.pathPicked.connect(file_label.setText)
        ttk.TTkHelper.overlay(wrap_widg, filePicker, 2, 1, True)
    # Bind File Picker buttons
    logo_btn.clicked.connect(lambda : _FilePickerDialog(ttk.TTkK.FileMode.AnyFile))
    favicon_btn.clicked.connect(lambda : _FilePickerDialog(ttk.TTkK.FileMode.Directory))

    # Buttons
    btn_widget = ttk.TTkFrame(layout= ttk.TTkGridLayout(columnMinWidth=1), border=0)
    btn_widget.setPadding(1,1,2,2)
    btn_cancel = ttk.TTkButton(text='Cancel')
    btn_save = ttk.TTkButton(text='Save')
    btn_widget.layout().addWidget(btn_cancel, 1, 0)
    btn_widget.layout().addWidget(btn_save, 1, 2)
    wrap_widg.layout().addWidget(btn_widget)

    # Button processors
    def _cancelBtn():
        nonlocal d_styles; nonlocal new_d_styles
        ligh_primary.setColor(ttk.TTkColor.bg(d_styles['light']['primary']))
        ligh_accent.setColor(ttk.TTkColor.bg(d_styles['light']['accent']))
        ligh_background.setColor(ttk.TTkColor.bg(d_styles['light']['background']))
        ligh_text.setColor(ttk.TTkColor.bg(d_styles['light']['text']))
        ligh_title.setColor(ttk.TTkColor.bg(d_styles['light']['title']))
        ligh_subtitle.setColor(ttk.TTkColor.bg(d_styles['light']['subtitle']))
        ligh_code.setColor(ttk.TTkColor.bg(d_styles['light']['code_text']))
        ligh_code_background.setColor(ttk.TTkColor.bg(d_styles['light']['code_background']))
        dark_primary.setColor(ttk.TTkColor.bg(d_styles['dark']['primary']))
        dark_accent.setColor(ttk.TTkColor.bg(d_styles['dark']['accent']))
        dark_background.setColor(ttk.TTkColor.bg(d_styles['dark']['background']))
        dark_text.setColor(ttk.TTkColor.bg(d_styles['dark']['text']))
        dark_title.setColor(ttk.TTkColor.bg(d_styles['dark']['title']))
        dark_subtitle.setColor(ttk.TTkColor.bg(d_styles['dark']['subtitle']))
        dark_code.setColor(ttk.TTkColor.bg(d_styles['dark']['code_text']))
        dark_code_background.setColor(ttk.TTkColor.bg(d_styles['dark']['code_background']))
        header_color.setColor(ttk.TTkColor.bg(d_styles['common_colors']['header']))
        nav_color.setColor(ttk.TTkColor.bg(d_styles['common_colors']['nav']))
        new_d_styles = copy.deepcopy(d_styles)
    def _savelBtn():
        nonlocal d_styles; nonlocal new_d_styles
        write_styles_scss(new_d_styles)
        d_styles = copy.deepcopy(new_d_styles)
    # Connect buttons
    btn_cancel.clicked.connect(lambda : _cancelBtn())    
    btn_save.clicked.connect(lambda : _savelBtn())

    return wrap_widg
