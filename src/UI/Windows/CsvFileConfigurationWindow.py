from src.UI.Base.Modal import Modal, ModalProps
from src.UI.Widgets.Dropdown import Dropdown

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel


class CsvFileConfigurationWindow(Modal):
    def __init__(self):
        super().__init__(ModalProps(Title="File Configuration"))
        layout = QVBoxLayout()
        buttonWidget = QWidget()
        buttonLayout = QHBoxLayout()
        buttonWidget.setLayout(buttonLayout)
        self.text = QLabel(
            "Please specify the following values to correctly load in the CSV file."
        )
        self.delimiterDropdown = Dropdown(
            "Delimiter",
            [r"\t", ",", ";", ".", "|", "-", "_"],
            choicesData=["\t", ",", ";", ".", "|", "-", "_"],
            labelWidth=80,
        )
        self.decimalDropdown = Dropdown(
            "Decimal", [",", ".", "_"], choicesData=[",", ".", "_"], labelWidth=80
        )
        self.okButton = QPushButton("OK")
        self.okButton.clicked.connect(self.Close)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.Close)
        layout.addWidget(self.text)
        layout.addWidget(self.delimiterDropdown)
        layout.addWidget(self.decimalDropdown)
        buttonLayout.addWidget(self.okButton)
        buttonLayout.addWidget(self.cancelButton)
        layout.addWidget(buttonWidget)
        self.setLayout(layout)
