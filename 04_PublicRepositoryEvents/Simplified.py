import tkinter as tk
from tkinter.constants import *
from functools import partial
from tkinter.messagebox import showinfo

def setGeometry(child, geometry_str):
    print(geometry_str)

def createWidget(master, widget_name, widget_type, geometry_str, **kwargs):
    class CustomWidget(widget_type):
        def __getattr__(self, item):
            return partial(createWidget, self, item)

    child = CustomWidget(master, **kwargs)
    setattr(master, widget_name, child)
    setGeometry(child, geometry_str)

    return child


class Application(tk.Frame):
    def __init__(self, title):
        super(Application, self).__init__()
        self.master.title(title)
        self.createWidgets()

    def createWidgets(self):
        pass

    def __getattr__(self, item):
        return partial(createWidget, self, item)


class App(Application):
    def createWidgets(self):
        self.message = "Congratulations!\nYou've found a sercet level!"
        self.F1(tk.LabelFrame, "1:0", text="Frame 1")
        self.F1.B1(tk.Button, "0:0/NW", text="1")
        self.F1.B2(tk.Button, "0:1/NE", text="2")
        self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
        self.F2(tk.LabelFrame, "1:1", text="Frame 2")
        self.F2.B1(tk.Button, "0:0/N", text="4")
        self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
        self.F2.B3(tk.Button, "1:0/S", text="6")
        self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
        self.F1.B3.bind("<Any-Key>", lambda event: showinfo(self.message.split()[0], self.message))

app = App(title="Sample application")
app.mainloop()