from src.Core.Log import Log
from src.Core.Core import ASSERT
from src.Logic.Line import LineManager, LineWithState
from src.UI.Base.Window import Window, WindowProps

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import math
from enum import Enum
import pandas
import matplotlib

matplotlib.use("Qt5Agg")

plt.rcParams["axes.formatter.use_locale"] = True
plt.rcParams["figure.autolayout"] = True
plt.rcParams["axes.linewidth"] = 1.5


class DIAGRAM_MODE(Enum):
    EDIT = 1
    PUBLISH = 2


class DiagramCreator:
    xUnit = None
    yUnit = None
    xBase = None
    yBase = None
    xBaseText = None
    yBaseText = None
    xBins = 8
    yBins = 5
    showLegend = False
    mode = DIAGRAM_MODE.EDIT

    def __init__(self):
        self.win = Window(
            windowProps=WindowProps(Title="Diagram View", Width=700, Height=400)
        )
        self.fig = Figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.win.setCentralWidget(self.canvas)
        self.lineManager = LineManager()

        self.axes = self.fig.add_subplot(111)

        self.axes.tick_params(
            axis="both",
            which="major",
            pad=8,
            direction="in",
            top=True,
            right=True,
            width=1.0,
            length=7,
            labelsize=14,
        )

        plt.rc(
            "legend", edgecolor="black", framealpha=1, handlelength=4, fancybox=False
        )

        self.axes.grid(
            linestyle=(0, [1, 10]),
            color=(60 / 255.0, 60 / 255.0, 60 / 255.0),
            linewidth=1,
        )

        self.axes.locator_params(axis="x", nbins=self.xBins)
        self.axes.locator_params(axis="y", nbins=self.yBins)

    def Clear(self):
        DiagramCreator.xUnit = None
        DiagramCreator.yUnit = None
        DiagramCreator.xBase = None
        DiagramCreator.yBase = None
        DiagramCreator.xBaseText = None
        DiagramCreator.yBaseText = None
        DiagramCreator.xBins = 8
        DiagramCreator.yBins = 5
        DiagramCreator.showLegend = False
        DiagramCreator.mode = DIAGRAM_MODE.EDIT
        self.axes.clear()
        self.axes.grid(
            linestyle=(0, [1, 10]),
            color=(60 / 255.0, 60 / 255.0, 60 / 255.0),
            linewidth=1,
        )
        self.fig.canvas.draw()

    def SoftClear(self):
        for line in self.axes.get_lines():
            line.remove()

    def GetCanvas(self):
        return self.canvas

    def PlotLine(self, line):
        self.axes.plot(
            line.x,
            line.y,
            label=line.label,
            color=line.color.value,
            marker=line.marker.value,
            markeredgecolor=line.markerColor.value,
            markerfacecolor=line.markerColorInner.value,
        )
        self.fig.canvas.draw()

    def AddLine(self, x, y, **kwargs):
        line = LineWithState(x, y, **kwargs)
        self.lineManager.AddLine(line)
        if line.active:
            self.PlotLine(line)
        return line.id

    def UpdateLine(self, id, redraw=True, **kwargs):
        self.lineManager.UpdateLine(id, **kwargs)
        if redraw:
            self.Redraw()

    def RemoveLine(self, lineID):
        ASSERT(False, "TODO: Implementation")  # TODO

    def SetLegend(self, show):
        if show:
            DiagramCreator.showLegend = True
            self.axes.legend(fontsize=14)
        else:
            DiagramCreator.showLegend = False
            try:
                self.axes.get_legend().remove()
            except:
                pass
        self.fig.canvas.draw()

    def SetTitle(self, title):
        self.title = title
        self.axes.set_title(title, fontsize=18)
        self.fig.canvas.draw()

    def SetXLabel(self, label):
        self.xLabel = label
        labelToSet = f"$\\rm{label}$ $\\longrightarrow$" if label else None
        self.axes.set_xlabel(labelToSet, fontsize=16, labelpad=12)
        self.fig.canvas.draw()

    def SetYLabel(self, label):
        self.yLabel = label
        labelToSet = f"$\\rm{label}$ $\\longrightarrow$" if label else None
        self.axes.set_ylabel(labelToSet, fontsize=16, labelpad=12)
        self.fig.canvas.draw()

    def SetXLowerLimit(self, value):
        self.xLowerLimit = value
        self.axes.set_xlim(xmin=value)
        self.fig.canvas.draw()

    def SetXUpperLimit(self, value):
        self.xUpperLimit = value
        self.axes.set_xlim(xmax=value)
        self.fig.canvas.draw()

    def SetYLowerLimit(self, value):
        self.yLowerLimit = value
        self.axes.set_ylim(ymin=value)
        self.fig.canvas.draw()

    def SetYUpperLimit(self, value):
        self.yUpperLimit = value
        self.axes.set_ylim(ymax=value)
        self.fig.canvas.draw()

    def SetXBins(self, xBins):
        self.xBins = xBins
        self.axes.locator_params(axis="x", nbins=self.xBins)
        self.fig.canvas.draw()

    def SetYBins(self, yBins):
        self.yBins = yBins
        self.axes.locator_params(axis="y", nbins=self.yBins)
        self.fig.canvas.draw()

    # Function only impacting publish mode

    def SetXBase(self, value):
        self.xBase = value
        self.fig.canvas.draw()

    def SetYBase(self, value):
        self.yBase = value
        self.fig.canvas.draw()

    def SetXUnit(self, unit):
        self.xUnit = unit
        self.fig.canvas.draw()

    def SetYUnit(self, unit):
        self.yUnit = unit
        self.fig.canvas.draw()

    def Redraw(self):
        self.SoftClear()

        for line in self.lineManager.GetLinesActive():
            self.PlotLine(line)

        # Toggle legend 2 times to trigger redraw
        self.SetLegend(not DiagramCreator.showLegend)
        self.SetLegend(not DiagramCreator.showLegend)
        self.fig.canvas.draw()

    def SetMode(self, diagramMode):
        self.mode = diagramMode

        if diagramMode == DIAGRAM_MODE.EDIT:
            self._ResetTickLabels("x")
            self._ResetTickLabels("y")
        elif diagramMode == DIAGRAM_MODE.PUBLISH:
            self._ManipulateTickLabels("x")
            self._ManipulateTickLabels("y")
        self.fig.canvas.draw()

    def Save(self, filepath):
        self.fig.savefig(filepath)
        return filepath

    def LoadCSV(self, filepath, delimiter, decimal):
        df = pandas.read_csv(filepath, delimiter=delimiter, decimal=decimal)
        x = df.iloc[:, 0].tolist()

        for i in range(1, len(df.columns.values)):
            y = df.iloc[:, i].astype(float).tolist()
            id = self.AddLine(x, y, label=df.columns.values[i])
            if i == 1:
                self.activeLineID = id
        self.Show()

    def Show(self):
        self.win.Show()

    def Close(self):
        plt.close(self.fig)

    def _ManipulateTickLabels(self, axe):
        ASSERT(axe in ["x", "y"], "Can only manipulate x or y axe!")

        if axe == "x":
            ticksAsNumbers = self.axes.get_xticks()
            unit = self.xUnit
            base = self.xBase
            basePos = {"x": 1.01, "y": 0.0}
        elif axe == "y":
            ticksAsNumbers = self.axes.get_yticks()
            unit = self.yUnit
            base = self.yBase
            basePos = {"x": 0.0, "y": 1.01}

        textHandle = None
        if base:
            if not math.log10(base).is_integer():
                Log.Error("base must be divisible by 10!")
            ticksAsNumbers = list(map(lambda x: x / float(base), ticksAsNumbers))
            exponent = int(math.floor(math.log10(abs(base)))) if base != 0 else 0
            textHandle = self.axes.text(
                x=basePos["x"],
                y=basePos["y"],
                s="$10^{" + str(exponent) + "}$",
                transform=self.axes.transAxes,
                fontsize=12,
            )

        formatString = "{:g}"
        ticks = [formatString.format(number) for number in ticksAsNumbers]

        # Zaehle max. Anzahl an Nachkommastellen
        maxAnzNachkommastellen = 0
        for val in ticks:
            try:
                nachkommastellen = len(val.split(".")[1])
                if nachkommastellen > maxAnzNachkommastellen:
                    maxAnzNachkommastellen = nachkommastellen
            except:
                pass

        # Erneut ticks als str erstellen (mit richtigem Format (Nachkommastellen) jetzt)
        formatString = "{:." + str(maxAnzNachkommastellen) + "f}"
        ticks = [formatString.format(number) for number in ticksAsNumbers]
        ticks = [x.replace(".", ",") for x in ticks]

        if unit:
            ticks[-2] = r"$\rm{%s}$" % unit

        if axe == "x":
            self.xBaseText = textHandle
            self.axes.set_xticklabels(ticks)
            self.axes.xaxis.get_ticklines()[0].set_visible(False)
            self.axes.xaxis.get_ticklines()[1].set_visible(False)
            self.axes.xaxis.get_ticklines()[-1].set_visible(False)
            self.axes.xaxis.get_ticklines()[-2].set_visible(False)
        elif axe == "y":
            self.yBaseText = textHandle
            self.axes.set_yticklabels(ticks)
            self.axes.yaxis.get_ticklines()[0].set_visible(False)
            self.axes.yaxis.get_ticklines()[1].set_visible(False)
            self.axes.yaxis.get_ticklines()[-1].set_visible(False)
            self.axes.yaxis.get_ticklines()[-2].set_visible(False)

    def _ResetTickLabels(self, axe):
        if axe == "x":
            axis = self.axes.xaxis
            baseTextToRemove = self.xBaseText
        elif axe == "y":
            axis = self.axes.yaxis
            baseTextToRemove = self.yBaseText
        axis.set_major_locator(mticker.AutoLocator())
        axis.set_major_formatter(mticker.ScalarFormatter())
        try:
            baseTextToRemove.remove()
        except:
            pass
