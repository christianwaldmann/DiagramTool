from PyQt5.QtWidgets import QHBoxLayout, QLabel, QComboBox, QWidget


class Dropdown(QWidget):
    def __init__(self, label, choices, labelWidth=None, *args, **kwargs):
        super(Dropdown, self).__init__(*args, **kwargs)
        layout = QHBoxLayout()
        self.label = QLabel(label)
        if labelWidth:
            self.label.setFixedWidth(labelWidth)
        layout.addWidget(self.label)

        self.dropdown = QComboBox()
        self.dropdown.addItems(choices)
        layout.addWidget(self.dropdown)

        self.setLayout(layout)

    def GetDropdown(self):
        return self.dropdown
