from src.Core.Log import Log

from dataclasses import dataclass

from PyQt5.QtWidgets import QDialog


@dataclass
class ModalProps:
    Title: str = "Modal"
    Width: int = 400
    Height: int = 200


class Modal(QDialog):
    def __init__(self, modalProps=ModalProps()):
        super().__init__()
        Log.Info(
            f"Creating modal {modalProps.Title} ({modalProps.Width}, {modalProps.Height})"
        )

        self.setModal(True)

        self.title = modalProps.Title
        self.setWindowTitle(self.title)

        self.width = modalProps.Width
        self.height = modalProps.Height
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
        self.exec_()

    def Hide(self):
        self.hide()

    def Close(self):
        self.close()
