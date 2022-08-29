import TermTk as ttk
from TermTk import TTkFrame, TTkWindow
from TermTk import TTkColor

# used !
def make_horizontal_pair(a, b):
    pf = ttk.TTkFrame(layout= ttk.TTkGridLayout(columnMinWidth=1), border=0)
    pf.layout().addWidget(a, 1, 0)
    pf.layout().addWidget(b, 1, 2)
    pf.setPadding(1,0,2,2)
    return pf


# not used
class ColorFrame(TTkFrame):
    __slots__ = ('_fillColor')
    def __init__(self, *args, **kwargs):
        TTkFrame.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_KolorFrame')
        self._fillColor = kwargs.get('fillColor', TTkColor.RST)

    def setFillColor(self, color):
        self._fillColor = color

    def paintEvent(self):
        w,h = self.size()
        for y in range(h):
            self._canvas.drawText(pos=(0,y),text='',width=w,color=self._fillColor)
        return super().paintEvent()


class ColorWindow(TTkWindow):
    __slots__ = ('_fillColor')
    def __init__(self, *args, **kwargs):
        TTkFrame.__init__(self, *args, **kwargs)
        self._name = kwargs.get('name' , '_KolorFrame')
        self._fillColor = kwargs.get('fillColor', TTkColor.RST)

    def setFillColor(self, color):
        self._fillColor = color

    def paintEvent(self):
        super().paintEvent()
        w,h = self.size()
        for y in range(h):
            self._canvas.drawText(pos=(0,y),text='',width=w,color=self._fillColor)
        return 