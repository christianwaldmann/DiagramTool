from enum import Enum
import codecs

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QComboBox, QWidget


class Mode(Enum):
    ITEM_TEXT_AS_VALUE = 1
    ITEM_DATA_AS_VALUE = 2


class Dropdown(QWidget):
    def __init__(
        self, label, choices, choicesData=None, labelWidth=None, *args, **kwargs
    ):
        super(Dropdown, self).__init__(*args, **kwargs)
        if choicesData:
            self.mode = Mode.ITEM_DATA_AS_VALUE
        else:
            self.mode = Mode.ITEM_TEXT_AS_VALUE
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(label)
        if labelWidth:
            self.label.setFixedWidth(labelWidth)
        layout.addWidget(self.label)

        self.dropdown = QComboBox()
        if self.mode == Mode.ITEM_DATA_AS_VALUE:
            for choice, choiceData in zip(choices, choicesData):
                self.dropdown.addItem(choice, choiceData)
        else:
            self.dropdown.addItems(choices)
        layout.addWidget(self.dropdown)

        self.setLayout(layout)

    def GetDropdown(self):
        return self.dropdown

    def GetValue(self):
        if self.mode == Mode.ITEM_DATA_AS_VALUE:
            return codecs.decode(
                self.dropdown.currentData(self.dropdown.currentIndex()),
                "unicode_escape",
            )
        else:
            return self.dropdown.currentText()
