import tkinter as tk
from tkinter.constants import *
from tkinter import colorchooser

class GraphicsEditor(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self._fillColor = "#000000"
        self._outlineColor = "#000000"
        self._outlineWidth = 1
        self._mousePushed = False
        self._figures = []
        self._activeFigure = None
        self._mouseMoveAction = None
        self._createWidgets()

    def _createWidgets(self):
        self.grid_rowconfigure(1, weight=1)
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
        self._fillColorButton = tk.Button(self, text='Fill Color', command=self._fillColorChange)
        self._fillColorButton.grid(row = 0, column=0, sticky="WE")
        self._outlineColorButton = tk.Button(self, text='Outline Color', command=self._outlineColorChange)
        self._outlineColorButton.grid(row=0, column=1, sticky="WE")
        self._outlineWidthBox = tk.Spinbox(self, width=5, from_=0, to=100, command=self._outlineWidthChanged)
        self._outlineWidthBox.grid(row = 0, column=2, sticky="WE")

        self._canvas = tk.Canvas(self)
        self._canvas.grid(row = 1, columnspan=3, sticky="NWSE")
        self._canvas.bind("<Button-1>",        self._mouseLeftButtonPress)
        self._canvas.bind("<ButtonRelease-1>", self._mouseLeftButtonRelease)
        self._canvas.bind("<Motion>",          self._mouseMove)

    def _outlineWidthChanged(self):
        self._outlineWidth = self._outlineWidthBox.get()

    def _fillColorChange(self):
        color_code = colorchooser.askcolor()
        self._fillColor = color_code[-1]

    def _outlineColorChange(self):
        color_code = colorchooser.askcolor()
        self._outlineColor = color_code[-1]

    def _mouseLeftButtonPress(self, event):
        self._mousePushed = True
        x, y = event.x, event.y

        ids = self._canvas.find_overlapping(x-1, y-1, x+1, y+1)
        if (len(ids) != 0):
            self._activeFigure = ids[-1], x, y
            self._mouseMoveAction = self._drag
        else:
            self._figures.append(self._canvas.create_oval(
                x, y, x, y,
                fill=self._fillColor,
                outline=self._outlineColor,
                width=self._outlineWidth))
            self._activeFigure = self._figures[-1], x, y
            self._mouseMoveAction = self._resize

    def _mouseLeftButtonRelease(self, event):
        self._mousePushed = False
        self._activeFigure = None
        self._mouseMoveAction = None

    def _mouseMove(self, event):
        if not self._mousePushed:
            return
        if self._mouseMoveAction is None:
            return

        self._mouseMoveAction(event.x, event.y)

    def _resize(self, x, y):
        id, x_static, y_static = self._activeFigure
        self._canvas.coords(id, min(x, x_static), min(y, y_static), max(x, x_static), max(y, y_static))

    def _drag(self, x, y):
        id, x_on_push, y_on_push = self._activeFigure
        offs_x = x - x_on_push
        offs_y = y - y_on_push
        x0, y0, x1, y1 = self._canvas.coords(id)
        self._canvas.coords(id, x0+offs_x, y0+offs_y, x1+offs_x, y1+offs_y)
        self._activeFigure = id, x, y

    def clear(self):
        self._canvas.delete("all")

class TextEditor(tk.LabelFrame):
    def __init__(self, master=None, title="Text Editor"):
        super().__init__(master)
        self.config(text=title)

    def _createWidgets(self):
        self.b = tk.Button(self, text='tex')
        self.b.grid()

class Application(tk.Frame):
    def __init__(self, master=None, title="<application>"):
        super().__init__(master)
        self.master.title(title)
        self.grid(sticky="NWSE")
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1, uniform="_")
        self.grid_columnconfigure(0, weight=1, uniform="_")
        self.grid_columnconfigure(1, weight=1, uniform="_")
        self.createWidgets()

    def createWidgets(self):
        self.textEditor = TextEditor(self, title="Text Editor EX")
        self.graphEditor = GraphicsEditor(self)
        self.clearButton = tk.Button(self, text="Clear", command=self.graphEditor.clear)
        self.textEditor.grid(row=0, column=0, sticky="NWSE")
        self.graphEditor.grid(row=0, column=1, sticky="NWSE")
        self.clearButton.grid(row=1, column=0, sticky="W")



app = Application(title="Graph Editor")
app.mainloop()