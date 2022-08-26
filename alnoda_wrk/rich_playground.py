import os
import sys

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.pretty import Pretty



console = Console()
text = Text("Hello, World!")
text.stylize("bold magenta", 0, 6)
console.print(text)

panel = Panel(Text("Hello", justify="right"))
console.print(panel)

pretty_locals = Pretty(locals())
console.print(pretty_locals)