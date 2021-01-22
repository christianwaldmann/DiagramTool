from src.Core.Color import COLOR
from src.Core.Marker import MARKER
from src.Core.Parser import EvalMathExpr

import uuid


class Line:
    def __init__(self, x, y, label="Unnamed Line"):
        self.x = x
        self.y = y
        self.label = label
        self.color = COLOR.BLACK
        self.marker = MARKER.NONE
        self.markerColor = COLOR.BLACK
        self.markerColorInner = COLOR.BLACK


#
#
# class LineMultiplicationData:
#     def __init__(self, multiplicationString="", evaluatedMultiplicationValue=1):
#         self.multiplicationString = multiplicationString
#         self.evaluatedMultiplicationValue = evaluatedMultiplicationValue


LineMultiplicationData = {"multiplicationString": "", "evaluatedMultiplicationValue": 1}


class LineWithState(Line):
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, **kwargs)
        self.xUnmodified = x
        self.yUnmodified = y
        self.id = uuid.uuid4()
        self.active = True
        self.xMultiplicationData = LineMultiplicationData
        self.yMultiplicationData = LineMultiplicationData


class LineManager:
    def __init__(self):
        self.linesWithState = []

    def AddLine(self, lineWithState):
        self.linesWithState.append(lineWithState)

    def GetLine(self, id):
        for lineWithState in self.linesWithState:
            if lineWithState.id == id:
                return lineWithState

    def GetLineIndex(self, id):
        for i, lineWithState in enumerate(self.linesWithState):
            if lineWithState.id == id:
                return i

    def GetLines(self):
        return self.linesWithState

    def GetLinesActive(self):
        activeLines = []
        for line in self.linesWithState:
            if line.active:
                activeLines.append(line)
        return activeLines

    def UpdateLine(
        self,
        id,
        x=None,
        y=None,
        active=None,
        label=None,
        color=None,
        marker=None,
        markerColor=None,
        markerColorInner=None,
        xMultiplicationData=None,
        yMultiplicationData=None,
    ):
        lineWithState = self.GetLine(id)
        if x:
            lineWithState.x = x
            lineWithState.xUnmodified = x
        if y:
            lineWithState.y = y
            lineWithState.yUnmodified = y
        if active != None:
            lineWithState.active = active
        if label:
            lineWithState.label = label
        if color:
            lineWithState.color = color
        if marker:
            lineWithState.marker = marker
        if markerColor:
            lineWithState.markerColor = markerColor
        if markerColorInner:
            lineWithState.markerColorInner = markerColorInner
        if xMultiplicationData:
            lineWithState.xMultiplicationData = xMultiplicationData
            f = xMultiplicationData["evaluatedMultiplicationValue"]
            if isinstance(f, float) or isinstance(f, int):
                lineWithState.x = [x * f for x in lineWithState.xUnmodified]
        if yMultiplicationData:
            lineWithState.yMultiplicationData = yMultiplicationData
            f = yMultiplicationData["evaluatedMultiplicationValue"]
            if isinstance(f, float) or isinstance(f, int):
                lineWithState.y = [y * f for y in lineWithState.yUnmodified]
