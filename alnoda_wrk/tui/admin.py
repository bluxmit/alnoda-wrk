import sys, os, argparse, math, random


def open_admin():
    """ Open interactive admin UI TUI """

    # Imports are inside a function because TermTk cannot be imported in the docker build phase
    # Imports will be called only when starting cli app
    import TermTk as ttk
    from TermTk.TTkCore.color import TTkColor
    from .home import WrkHomeTab
    from .features_widget import get_features_widget
    from .description_widget import get_description_widget
    from .preferences_widget import get_preferences_widget
    from .interface_widget import get_interface_widget
    from .apps_services import get_apps_services_widget
    from .env_vars_widget import get_env_vars_widget
    from .aliases_widget import get_aliases_widget

    options = ["Home", "Features", "Description", "Preferences", "Intrerface", "Apps & Services", "Env variables", "Aliases"]


    def AlnodaAdminTUI(root= None):
        # ttk.TTkLogViewer(parent=root)
        frame = ttk.TTkFrame(parent=root, border=False)

        # Create internal window
        w = root._width; h = root._height
        mw = 140; mh = 30; mx = int((w - mw)/2); my = int((h - mh)/2)
        mainw = ttk.TTkWindow(parent=frame, size=(mw,mh), pos=(mx,my), title="Alnoda admin", border=True, layout=ttk.TTkGridLayout(), maxWidth=mw, minWidth=mw, maxHeight=mh, minHeight=mh)

        splitter = ttk.TTkSplitter(parent=mainw, orientation=ttk.TTkK.HORIZONTAL)
        leftFrame = ttk.TTkFrame(parent=splitter, border=0, layout=ttk.TTkVBoxLayout())
        RightFrame = ttk.TTkFrame(parent=splitter, border=0, layout=ttk.TTkVBoxLayout())
        
        # Selection List
        listWidget = ttk.TTkList(maxWidth=20, minWidth=20)
        listWidget.setPadding(1,1,1,1)
        leftFrame.layout().addWidget(listWidget)

        # Home tab
        hello_widget = WrkHomeTab(border=0)
        r_widget = hello_widget
        RightFrame.layout().addWidget(hello_widget)

        # FeaturesWidget
        FeaturesWidget = get_features_widget()
        RightFrame.layout().addWidget(FeaturesWidget)

        # DescriptionWidget
        DescriptionWidget = get_description_widget()
        RightFrame.layout().addWidget(DescriptionWidget)

        # InterfaceWidget
        InterfaceWidget = get_interface_widget()
        RightFrame.layout().addWidget(InterfaceWidget)

        # AppsServicesWidget
        AppsServicesWidget = get_apps_services_widget()
        RightFrame.layout().addWidget(AppsServicesWidget)

        # EnvVarsWidget
        EnvVarsWidget = get_env_vars_widget()
        RightFrame.layout().addWidget(EnvVarsWidget)

        # AliasesWidget
        AliasesWidget = get_aliases_widget()
        RightFrame.layout().addWidget(AliasesWidget)

        @ttk.pyTTkSlot(str)
        def _listCallback(label):
            widget = None
            if   label == "Home":               widget = hello_widget
            elif label == "Features":           widget = FeaturesWidget
            elif label == "Description":        widget = DescriptionWidget
            elif label == "Intrerface":         widget = InterfaceWidget
            elif label == "Apps & Services":    widget = AppsServicesWidget
            elif label == "Env variables":      widget = EnvVarsWidget
            elif label == "Aliases":            widget = AliasesWidget
            elif label == "Preferences":    
                widget = get_preferences_widget()
                RightFrame.layout().addWidget(widget)
                widget.show()
            if widget:
                if _listCallback.active:
                    _listCallback.active.hide()
                widget.show()
                _listCallback.active = widget
        _listCallback.active = None

        # Connect the signals to the 2 slots defines
        listWidget.textClicked.connect(_listCallback)
        listWidget.setCurrentRow(1)

        # populate the lists with random entries
        for option in options:
            listWidget.addItem(f"{option}")
        return splitter


    # Launch admin TUI app
    root = ttk.TTk()
    root.setLayout(ttk.TTkGridLayout())
    AlnodaAdminTUI(root)
    root.mainloop()


