import TermTk as ttk
from TermTk.TTkCore.string import TTkString

from .env_vars_widget import get_env_vars_widget
from .aliases_widget import get_aliases_widget



def get_zsh_widget():
    wrap_widg = ttk.TTkFrame(layout=ttk.TTkVBoxLayout(columnMinHeight=1), border=0, visible=False)
    tabArea = ttk.TTkTabWidget(minHeight=15, border=True)
    wrap_widg.layout().addWidget(tabArea)

    # Create tabs
    EnvVarsScrollArea = get_env_vars_widget()
    tabArea.addTab(EnvVarsScrollArea,  "Env vars")

    AliasesScrollArea = get_aliases_widget()
    tabArea.addTab(AliasesScrollArea,  "Aliases")

    return wrap_widg