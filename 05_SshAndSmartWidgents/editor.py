import tkinter as tk
from tkinter.constants import *
from tkinter import colorchooser
import re

class GraphicsEditor(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self._fillColor = "#000000"
        self._outlineColor = "#000000"
        self._outlineWidth = 0
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
        self.focus_set()
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
        self._updateText()

    def _mouseMove(self, event):
        if not self._mousePushed:
            return
        if self._mouseMoveAction is None:
            return

        self._mouseMoveAction(event.x, event.y)
        self._updateText()

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
        self._figures = []

    def _serializeFigure(self, id):
        x0, y0, x1, y1 = self._canvas.coords(id)
        outlineWidth = self._canvas.itemcget(id, "width")
        outlineColor = self._canvas.itemcget(id, "outline")
        fillColor = self._canvas.itemcget(id, "fill")
        return f"<{x0} {y0} {x1} {y1}> {outlineWidth} {outlineColor} {fillColor}"

    def _updateText(self):
        serializedObjects = [self._serializeFigure(id) for id in self._figures]
        self.master.updateText(serializedObjects)

    def updateObjects(self, serializedObjects):
        self.clear()
        for obj in serializedObjects:
            self._figures.append(self._canvas.create_oval(
                obj['x0'], obj['y0'], obj['x1'], obj['y1'],
                fill=obj['fillColor'],
                outline=obj['outlineColor'],
                width=obj['outlineWidth']))


class TextEditor(tk.LabelFrame):
    def __init__(self, master=None, title="Text Editor"):
        super().__init__(master)
        self.config(text=title)
        self._createWidgets()
        self._tagErrors = "errors"
        self._textWidget.tag_config(self._tagErrors, background="red")
        self._updatedFromGraphics = False

    def _createWidgets(self):
        self.grid_rowconfigure(0, weight=1, uniform="_")
        self.grid_columnconfigure(0, weight=1, uniform="_")
        self._textWidget = tk.Text(self, undo=True, wrap=tk.WORD, font="fixed",
                inactiveselectbackground="MidnightBlue")
        self._textWidget.grid(row=0, column=0, sticky="NWSE")
        self._textWidget.bind('<<Modified>>', self._analyseText)

    def clear(self):
        self._textWidget.delete("1.0", tk.END)

    def _loadLines(self):
        return self._textWidget.get("1.0", tk.END).split('\n')

    def _parseLine(self, line):
        params = re.match(
            r"<"                                          r"[\s]*"
            r"(?P<x0>[+\-]?(\d+(\.\d+)?))"                r"[\s]+"
            r"(?P<y0>[+\-]?(\d+(\.\d+)?))"                r"[\s]+"
            r"(?P<x1>[+\-]?(\d+(\.\d+)?))"                r"[\s]+"
            r"(?P<y1>[+\-]?(\d+(\.\d+)?))"                r"[\s]*"
            r">"                                          r"[\s]*"
            r"(?P<outlineWidth>[+\-]?(\d+(\.\d+)?))"      r"[\s]+"
            r"(?P<outlineColor>#?\w+)"                    r"[\s]+"
            r"(?P<fillColor>#?\w+)"                       r"[\s]*",
            line
        )
        if params is None:
            return None
        params = params.groupdict()
        try:
            self.winfo_rgb(params['outlineColor'])
            self.winfo_rgb(params['fillColor'])
        except tk.TclError:
            return None

        params['x0'] = float(params['x0'])
        params['y0'] = float(params['y0'])
        params['x1'] = float(params['x1'])
        params['y1'] = float(params['y1'])
        params['outlineWidth'] = float(params['outlineWidth'])
        return params

    # <1 2 3 4> 10 #000000 #000000

    def _analyseText(self, event):
        if self._textWidget.edit_modified() == 0:
            return
        if self._updatedFromGraphics:
            self._updatedFromGraphics = False
            self._textWidget.edit_modified(False)
            return

        lines = self._loadLines()
        serializedObjects = [self._parseLine(line) for line in lines if line != ""]
        if not self._markErrorLines(serializedObjects):
            self.master.updateGraphics(serializedObjects)

        self._textWidget.edit_modified(False)

    def _markErrorLines(self, serializedObjects):
        self._textWidget.tag_remove(self._tagErrors, "1.0", tk.END)
        serializedObjects = enumerate(serializedObjects)
        errorLinesInds = [i + 1 for i, obj in serializedObjects if obj is None]
        for i in errorLinesInds:
            self._textWidget.tag_add(self._tagErrors, f"{i}.0", f"{i}.end")

        return len(errorLinesInds) != 0

    def updateText(self, serializedObjects):
        self.clear()
        text = "\n".join(serializedObjects)
        self._updatedFromGraphics = True
        self._textWidget.insert("1.0", text)

class Application(tk.Frame):
    def __init__(self, master=None, title="<application>"):
        super().__init__(master)
        self.master.title(title)
        self.grid(sticky="NWSE")
        self.bind("<Button-1>", lambda event: self.focus_set())
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1, uniform="_")
        self.grid_columnconfigure(0, weight=1, uniform="_")
        self.grid_columnconfigure(1, weight=1, uniform="_")
        self.createWidgets()

    def createWidgets(self):
        self.textEditor = TextEditor(self, title="Text Editor")
        self.graphEditor = GraphicsEditor(self)
        self.clearButton = tk.Button(self, text="Clear", command=self.clear)
        self.textEditor.grid(row=0, column=0, sticky="NWSE")
        self.graphEditor.grid(row=0, column=1, sticky="NWSE")
        self.clearButton.grid(row=1, column=0, sticky="W")

    def clear(self):
        self.textEditor.clear()
        self.graphEditor.clear()

    def updateText(self, serializedObjects):
        self.textEditor.updateText(serializedObjects)

    def updateGraphics(self, serializedObjects):
        self.graphEditor.updateObjects(serializedObjects)


app = Application(title="Graph Editor")
app.mainloop()