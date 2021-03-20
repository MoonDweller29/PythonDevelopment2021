import tkinter as tk
from tkinter.constants import *
from functools import partial
from tkinter.messagebox import showinfo

def parseAxisSettings(axis_str):
    weight = 1
    span = 1

    span_ind = axis_str.find("+")
    if (span_ind >= 0):
        span = int(axis_str[span_ind+1 : ]) + 1
        axis_str = axis_str[:span_ind]

    weight_ind = axis_str.find(".")
    if (weight_ind >= 0):
        weight = int(axis_str[weight_ind+1 :])
        axis_str = axis_str[:weight_ind]

    ind = int(axis_str)

    return (ind, weight, span)


def parseGeometryStr(geometry_str):
    sticky = "NEWS"
    gravity_ind = geometry_str.find("/")
    if (gravity_ind >= 0):
        sticky = geometry_str[gravity_ind + 1 :]
        geometry_str = geometry_str[: gravity_ind]

    axis_splitter_ind = geometry_str.find(":")
    row_params = parseAxisSettings(geometry_str[:axis_splitter_ind])
    column_params = parseAxisSettings(geometry_str[axis_splitter_ind+1 :])

    return (row_params, column_params, sticky)

def setGeometry(child, geometry_str):
    row_params, column_params, sticky = parseGeometryStr(geometry_str)
    child.grid(row=row_params[0], rowspan=row_params[2],
               column=column_params[0], columnspan=column_params[2], sticky=sticky)
    child.master.grid_rowconfigure(row_params[0], weight=row_params[1])
    child.master.grid_columnconfigure(column_params[0], weight=column_params[1])

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
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.grid(sticky="NWSE")
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