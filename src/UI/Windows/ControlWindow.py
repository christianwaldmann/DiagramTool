from src.UI.Base.Window import Window
from src.UI.Widgets.Input import Input, Input2, InputNumber
from src.UI.Widgets.NavigationToolbar import NavigationToolbar
from src.UI.Widgets.Dropdown import Dropdown
from src.UI.Windows.CsvFileConfigurationWindow import CsvFileConfigurationWindow
from src.Logic.DiagramCreator import DIAGRAM_MODE
from src.Core.Parser import CastToNumberIfPossible, EvalMathExpr
from src.Core.Log import Log
from src.Core.Color import StringToColor
from src.Core.Marker import StringToMarker


from PyQt5.QtWidgets import (
    QGridLayout,
    QVBoxLayout,
    QWidget,
    QCheckBox,
    QComboBox,
    QGroupBox,
    QMenuBar,
    QFileDialog,
    QMessageBox,
)
import os
from matplotlib.backends.qt_compat import QtCore


class ControlWindow(Window):
    def __init__(self, windowProps, diagramCreator):
        super().__init__(windowProps)

        self.activeLineID = None
        self.saveFilepath = None
        self.diagramCreator = diagramCreator

        # Menubar
        menubar = QMenuBar()
        self.setMenuBar(menubar)
        fileMenu = menubar.addMenu("File")
        self.openMenubarAction = fileMenu.addAction(
            "Open...", lambda *args: None, "Ctrl+O"
        )
        self.saveMenubarAction = fileMenu.addAction(
            "Save", lambda *args: None, "Ctrl+S"
        )
        self.saveAsMenubarAction = fileMenu.addAction(
            "Save As...", lambda *args: None, "Ctrl+Shift+S"
        )
        fileMenu.addSeparator()
        self.exitMenubarAction = fileMenu.addAction("Exit")
        editMenu = menubar.addMenu("Edit")
        self.clearDiagramMenubarAction = editMenu.addAction("Clear Diagram")
        windowMenu = menubar.addMenu("Window")
        self.showDiagramViewWindowMenubarAction = windowMenu.addAction("Diagram View")

        self.toolbar = NavigationToolbar(self.diagramCreator.GetCanvas(), self)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)

        labelWidth = 100
        self.legendCheckbox = QCheckBox("Legend")
        self.titleInput = Input("Titel", "", labelWidth=labelWidth)
        self.xLabelInput = Input("X Label", "", labelWidth=labelWidth)
        self.yLabelInput = Input("Y Label", "", labelWidth=labelWidth)
        self.xUnitInput = Input("X Unit", "", labelWidth=labelWidth)
        self.yUnitInput = Input("Y Unit", "", labelWidth=labelWidth)
        self.xLimitInput = Input2("X Limit", "", "", labelWidth=labelWidth)
        self.yLimitInput = Input2("Y Limit", "", "", labelWidth=labelWidth)
        self.xBaseInput = Input("X Base", "", labelWidth=labelWidth)
        self.yBaseInput = Input("Y Base", "", labelWidth=labelWidth)
        self.mulitplyXValuesInput = Input(
            "Mulitply X Values", "", labelWidth=labelWidth
        )
        self.xBinsInput = InputNumber("Max Amount X Ticks", 8, labelWidth=labelWidth)
        self.yBinsInput = InputNumber("Max Amount Y Ticks", 5, labelWidth=labelWidth)

        self.toggleModeCheckbox = QCheckBox(
            "Publish Mode (Don't modify the plot afterwards)"
        )

        self.lineDropdown = QComboBox()
        self.lineActiveCheckbox = QCheckBox("Hide")
        self.lineLabelInput = Input("Label", "")
        self.lineColorDropdown = Dropdown(
            "Color", ["black", "red", "blue", "green", "orange", "tomato"]
        )
        self.lineMarkerDropdown = Dropdown("Marker", ["None", "d", "x", "+"])
        self.lineMarkerColorDropdown = Dropdown(
            "Marker Color",
            ["black", "white", "red", "blue", "green", "orange", "tomato"],
        )
        self.lineInnerMarkerColorDropdown = Dropdown(
            "Marker Inner Color",
            ["black", "white", "red", "blue", "green", "orange", "tomato"],
        )
        self.mulitplyYValuesInput = Input(
            "Mulitply Y Values", "", labelWidth=labelWidth
        )

        generalGroupBox = QGroupBox("General Settings")
        generalLayout = QVBoxLayout(generalGroupBox)
        generalLayout.addWidget(self.legendCheckbox)
        generalLayout.addWidget(self.titleInput)
        generalLayout.addWidget(self.xLabelInput)
        generalLayout.addWidget(self.yLabelInput)
        generalLayout.addWidget(self.xUnitInput)
        generalLayout.addWidget(self.yUnitInput)
        generalLayout.addWidget(self.xLimitInput)
        generalLayout.addWidget(self.yLimitInput)
        generalLayout.addWidget(self.xBaseInput)
        generalLayout.addWidget(self.yBaseInput)
        generalLayout.addWidget(self.mulitplyXValuesInput)
        generalLayout.addWidget(self.xBinsInput)
        generalLayout.addWidget(self.yBinsInput)

        modifyLineGroupBox = QGroupBox("Line Settings")
        modifyLineLayout = QVBoxLayout()
        modifyLineLayout.addWidget(self.lineDropdown)
        modifyLineLayout.addWidget(self.lineActiveCheckbox)
        modifyLineLayout.addWidget(self.lineLabelInput)
        modifyLineLayout.addWidget(self.lineColorDropdown)
        modifyLineLayout.addWidget(self.lineMarkerDropdown)
        modifyLineLayout.addWidget(self.lineMarkerColorDropdown)
        modifyLineLayout.addWidget(self.lineInnerMarkerColorDropdown)
        modifyLineLayout.addWidget(self.mulitplyYValuesInput)
        modifyLineGroupBox.setLayout(modifyLineLayout)

        mainWidget = QWidget()
        self.setCentralWidget(mainWidget)
        layout = QGridLayout(mainWidget)
        layout.addWidget(generalGroupBox, 0, 0)
        layout.addWidget(modifyLineGroupBox, 0, 1)
        layout.addWidget(self.toggleModeCheckbox, 1, 0, 1, 2)

        self.ConnectSignals()

    def ConnectSignals(self):
        self.openMenubarAction.triggered.connect(self.OnOpenMenubarActionClicked)
        self.saveMenubarAction.triggered.connect(self.OnSaveMenubarActionClicked)
        self.saveAsMenubarAction.triggered.connect(self.OnSaveAsMenubarActionClicked)
        self.exitMenubarAction.triggered.connect(self.OnExitMenubarActionClicked)
        self.clearDiagramMenubarAction.triggered.connect(
            self.OnClearDiagramMenubarActionClicked
        )
        self.showDiagramViewWindowMenubarAction.triggered.connect(
            self.OnShowDiagramViewWindowMenubarActionClicked
        )
        self.toggleModeCheckbox.stateChanged.connect(self.OnToggleModeCheckboxClicked)
        self.lineActiveCheckbox.stateChanged.connect(self.OnLineActiveCheckboxClicked)
        self.toggleModeCheckbox.stateChanged.connect(self.OnToggleModeCheckboxClicked)
        self.legendCheckbox.stateChanged.connect(self.OnLegendCheckboxClicked)
        self.xLimitInput.GetInput1().textChanged.connect(self.OnXLowerLimitChanged)
        self.xLimitInput.GetInput2().textChanged.connect(self.OnXUpperLimitChanged)
        self.yLimitInput.GetInput1().textChanged.connect(self.OnYLowerLimitChanged)
        self.yLimitInput.GetInput2().textChanged.connect(self.OnYUpperLimitChanged)
        self.xUnitInput.GetInput().textChanged.connect(self.OnXUnitChanged)
        self.yUnitInput.GetInput().textChanged.connect(self.OnYUnitChanged)
        self.xLabelInput.GetInput().textChanged.connect(self.OnXLabelChanged)
        self.yLabelInput.GetInput().textChanged.connect(self.OnYLabelChanged)
        self.titleInput.GetInput().textChanged.connect(self.OnTitleChanged)
        self.xBaseInput.GetInput().textChanged.connect(self.OnXBaseChanged)
        self.yBaseInput.GetInput().textChanged.connect(self.OnYBaseChanged)
        self.mulitplyXValuesInput.GetInput().textChanged.connect(
            self.OnMulitplyXValuesChanged
        )
        self.xBinsInput.GetInput().valueChanged.connect(self.OnXBinsChanged)
        self.yBinsInput.GetInput().valueChanged.connect(self.OnYBinsChanged)
        self.mulitplyYValuesInput.GetInput().textChanged.connect(
            self.OnMulitplyYValuesChanged
        )
        self.lineLabelInput.GetInput().textChanged.connect(self.OnLabelInputChanged)
        self.lineDropdown.currentIndexChanged.connect(
            self.OnLineDropdownSelectionChanged
        )
        self.lineColorDropdown.GetDropdown().currentTextChanged.connect(
            self.OnLineColorChanged
        )
        self.lineMarkerDropdown.GetDropdown().currentTextChanged.connect(
            self.OnLineMarkerChanged
        )
        self.lineMarkerColorDropdown.GetDropdown().currentTextChanged.connect(
            self.OnLineMarkerColorChanged
        )
        self.lineInnerMarkerColorDropdown.GetDropdown().currentTextChanged.connect(
            self.OnLineInnerMarkerColorChanged
        )

    def OnToggleModeCheckboxClicked(self, int):
        if int == 2:
            self.diagramCreator.SetMode(DIAGRAM_MODE.PUBLISH)
            self.toolbar.DisableMoving()
        else:
            self.diagramCreator.SetMode(DIAGRAM_MODE.EDIT)
            self.toolbar.EnableMoving()

    def OnLegendCheckboxClicked(self, int):
        if int == 2:
            self.diagramCreator.SetLegend(True)
        else:
            self.diagramCreator.SetLegend(False)

    def OnLineActiveCheckboxClicked(self, int):
        if int == 2:
            self.diagramCreator.UpdateLine(self.activeLineID, active=False)
        else:
            self.diagramCreator.UpdateLine(self.activeLineID, active=True)

    def OnXLowerLimitChanged(self, str):
        self.diagramCreator.SetXLowerLimit(CastToNumberIfPossible(str))

    def OnXUpperLimitChanged(self, str):
        self.diagramCreator.SetXUpperLimit(CastToNumberIfPossible(str))

    def OnYLowerLimitChanged(self, str):
        self.diagramCreator.SetYLowerLimit(CastToNumberIfPossible(str))

    def OnYUpperLimitChanged(self, str):
        self.diagramCreator.SetYUpperLimit(CastToNumberIfPossible(str))

    def OnXUnitChanged(self, str):
        self.diagramCreator.SetXUnit(str)

    def OnYUnitChanged(self, str):
        self.diagramCreator.SetYUnit(str)

    def OnTitleChanged(self, str):
        self.diagramCreator.SetTitle(str)

    def OnXLabelChanged(self, str):
        self.diagramCreator.SetXLabel(str)

    def OnYLabelChanged(self, str):
        self.diagramCreator.SetYLabel(str)

    def OnXBaseChanged(self, str):
        self.diagramCreator.SetXBase(CastToNumberIfPossible(str))

    def OnYBaseChanged(self, str):
        self.diagramCreator.SetYBase(CastToNumberIfPossible(str))

    def OnXBinsChanged(self, value):
        self.diagramCreator.SetXBins(value)

    def OnYBinsChanged(self, value):
        self.diagramCreator.SetYBins(value)

    def OnMulitplyXValuesChanged(self, str):
        evaluatedMultiplicationValue = EvalMathExpr(str)
        for line in self.diagramCreator.lineManager.GetLines():
            self.diagramCreator.UpdateLine(
                line.id,
                xMultiplicationData={
                    "multiplicationString": str,
                    "evaluatedMultiplicationValue": evaluatedMultiplicationValue,
                },
                redraw=False,
            )
        self.diagramCreator.Redraw()

    def OnMulitplyYValuesChanged(self, str):
        self.diagramCreator.UpdateLine(
            self.activeLineID,
            yMultiplicationData={
                "multiplicationString": str,
                "evaluatedMultiplicationValue": EvalMathExpr(str),
            },
        )

    def OnOpenMenubarActionClicked(self):
        dialog = QFileDialog()
        filepath, _ = dialog.getOpenFileName(
            filter="Comma Separated Values (*.csv);;All files (*)"
        )

        if filepath == "":
            return

        Log.Info(f"Reading in {filepath}")
        extension = os.path.splitext(filepath)[1]
        if extension == ".csv":

            self.fileConfigurationWindow = CsvFileConfigurationWindow()
            self.fileConfigurationWindow.Show()

            self.diagramCreator.LoadCSV(
                filepath,
                delimiter=self.fileConfigurationWindow.delimiterDropdown.GetValue(),
                decimal=self.fileConfigurationWindow.decimalDropdown.GetValue(),
            )
            for line in self.diagramCreator.lineManager.GetLines():
                self.lineDropdown.addItem(line.label)
            return

        Log.Warn(f"Attempted to open file with unsupported file format ({extension})")
        warnDialog = QMessageBox()
        warnDialog.setWindowTitle("Warning")
        warnDialog.setText(
            f'Could not open file!\nUnsupported file format: "{extension}"'
        )
        warnDialog.setDetailedText(
            f'Attempted to open file "{filepath}" with unsupported file format "{extension}"'
        )
        warnDialog.exec_()

    def OnSaveMenubarActionClicked(self):
        if self.saveFilepath:
            self.diagramCreator.Save(self.saveFilepath)
        else:
            self.saveFilepath = self._GetFilepathSaveFileDialog()
            self.diagramCreator.Save(self.saveFilepath)

    def OnSaveAsMenubarActionClicked(self):
        self.saveFilepath = self._GetFilepathSaveFileDialog()
        self.diagramCreator.Save(self.saveFilepath)

    def _GetFilepathSaveFileDialog(self):
        dialog = QFileDialog()
        filepath, _ = dialog.getSaveFileName(
            filter="Scalable Vector Graphics (*.svg);;Portable Network Graphics (*.png);;Joint Photographic Experts Group (*.jpg *.jpeg);;Portable Document Format (*.pdf);;All files (*)"
        )
        return filepath

    def OnExitMenubarActionClicked(self):
        self.diagramCreator.Close()
        self.Close()

    def OnShowDiagramViewWindowMenubarActionClicked(self):
        self.diagramCreator.Show()

    def OnClearDiagramMenubarActionClicked(self):
        self.diagramCreator.Clear()
        self.lineLabelInput.GetInput().setText("")
        self.lineDropdown.clear()

    def OnLabelInputChanged(self, str):
        self.diagramCreator.UpdateLine(self.activeLineID, label=str)
        i = self.diagramCreator.lineManager.GetLineIndex(self.activeLineID)
        self.lineDropdown.setItemText(i, str)

    def OnLineColorChanged(self, str):
        self.diagramCreator.UpdateLine(self.activeLineID, color=StringToColor(str))

    def OnLineMarkerChanged(self, str):
        self.diagramCreator.UpdateLine(self.activeLineID, marker=StringToMarker(str))

    def OnLineMarkerColorChanged(self, str):
        self.diagramCreator.UpdateLine(
            self.activeLineID, markerColor=StringToColor(str)
        )

    def OnLineInnerMarkerColorChanged(self, str):
        self.diagramCreator.UpdateLine(
            self.activeLineID, markerColorInner=StringToColor(str)
        )

    def OnLineDropdownSelectionChanged(self, i):
        try:
            activeLine = self.diagramCreator.lineManager.GetLines()[i]
            self.activeLineID = activeLine.id
            self.lineActiveCheckbox.setChecked(not activeLine.active)
            self.lineLabelInput.GetInput().setText(activeLine.label)
            self.lineMarkerDropdown.GetDropdown().setCurrentText(activeLine.marker)
            self.lineColorDropdown.GetDropdown().setCurrentText(activeLine.color)
            self.lineMarkerColorDropdown.GetDropdown().setCurrentText(
                activeLine.markerColor
            )
            self.lineInnerMarkerColorDropdown.GetDropdown().setCurrentText(
                activeLine.markerColorInner
            )
            self.mulitplyYValuesInput.GetInput().setText(
                activeLine.yMultiplicationString
            )
        except:
            pass
