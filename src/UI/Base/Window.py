from src.Core.Log import Log

from dataclasses import dataclass

from PyQt5.QtWidgets import QMainWindow, QApplication


@dataclass
class WindowProps:
    Title: str = "Window"
    Width: int = 1280
    Height: int = 720


class Window(QMainWindow):
    def __init__(self, windowProps=WindowProps()):
        self.app = QApplication([windowProps.Title])
        super().__init__()
        Log.Info(
            f"Creating window {windowProps.Title} ({windowProps.Width}, {windowProps.Height})"
        )

        self.title = windowProps.Title
        self.setWindowTitle(self.title)

        self.width = windowProps.Width
        self.height = windowProps.Height
        self.resize(self.width, self.height)

    def GetWidth(self):
        return self.width

    def SetWidth(self, width):
        self.width = width
        self.resize(self.width, self.height)

    def GetHeight(self):
        return self.height

    def SetHeight(self, height):
        self.height = height
        self.resize(self.width, self.height)

    def Show(self):
        self.show()

    def Hide(self):
        self.hide()

    def Close(self):
        self.close()
