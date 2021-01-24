try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import re


class TransparentWin(tk.Tk):
    """
    Transparent Tkinter Window Class.
    Based on martineau's comment @ Stack Overflow
    https://stackoverflow.com/questions/6104991/transparent-colors-tkinter
    """
    def __init__(self):

        tk.Tk.__init__(self)

        self.Drag = Drag(self)
        self.focus_force()
        self.overrideredirect(True)
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)
        self.attributes("-alpha", 0.8)
        self.wm_geometry('+' + str(1000) + '+' + str(172))
        bg = '#FFFFFF'
        self.config(bg=bg)
        # A dummy frame just so the window is clickable. For debug purposes
        # self.Frame = tk.Frame(self, bg=bg)
        # self.Frame.config(width=69, height=69)
        # self.Frame.pack(fill=tk.X)
        # self.Frame.bind('<Button-3>', self.exit)

    def exit(self, event):
        self.destroy()

    def position(self):
        _filter = re.compile(r"(\d+)?x?(\d+)?([+-])(\d+)([+-])(\d+)")
        pos = self.winfo_geometry()
        filtered = _filter.search(pos)
        self.X = int(filtered.group(4))
        self.Y = int(filtered.group(6))

        return self.X, self.Y

    def start_event_loop(self):
        self.mainloop()


class Drag:
    """ Makes a window dragable. """

    def __init__(self, par, dissable=None, releasecmd=None):
        self.Par        = par
        self.Dissable   = dissable
        self.ReleaseCMD = releasecmd

        self.Par.bind('<Button-1>', self.relative_position)
        self.Par.bind('<ButtonRelease-1>', self.drag_unbind)

    def relative_position(self, event):
        cx, cy = self.Par.winfo_pointerxy()
        x, y = self.Par.position()
        self.OriX = x
        self.OriY = y
        self.RelX = cx - x
        self.RelY = cy - y
        self.Par.bind('<Motion>', self.drag_wid)

    def drag_wid(self, event):
        cx, cy = self.Par.winfo_pointerxy()
        d = self.Dissable

        if d == 'x':
            x = self.OriX
            y = cy - self.RelY
        elif d == 'y':
            x = cx - self.RelX
            y = self.OriY
        else:
            x = cx - self.RelX
            y = cy - self.RelY

        if x < 0:
            x = 0
        if y < 0:
            y = 0

        self.Par.wm_geometry('+' + str(x) + '+' + str(y))

    def drag_unbind(self, event):
        self.Par.unbind('<Motion>')
        if self.ReleaseCMD != None:
            self.ReleaseCMD()

    def dissable(self):
        self.Par.unbind('<Button-1>')
        self.Par.unbind('<ButtonRelease-1>')
        self.Par.unbind('<Motion>')


def __run__():
    my_window = TransparentWin()
    my_window.mainloop()


if __name__ == '__main__':
    __run__()
