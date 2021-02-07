from src.UI.Windows.ControlWindow import ControlWindow
from src.UI.Base.Window import WindowProps

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui


class DiagramCreatorUI(QApplication):
    def __init__(self, diagramCreator):
        self.diagramCreator = diagramCreator
        super(QApplication, self).__init__([""])
        self.setWindowIcon(QtGui.QIcon("assets/icons/pikachu.svg"))

        self.controlWindow = ControlWindow(
            WindowProps(Title="Diagram Tool", Width=500, Height=500),
            self.diagramCreator,
        )
        self.controlWindow.Show()

    def Run(self):
        return self.exec_()
