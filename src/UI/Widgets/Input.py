from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QLineEdit, QSpinBox


class Input(QWidget):
    def __init__(self, label, initialText, labelWidth=None, *args, **kwargs):
        super(Input, self).__init__(*args, **kwargs)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(label)
        if labelWidth:
            self.label.setFixedWidth(labelWidth)
        layout.addWidget(self.label)

        self.input = QLineEdit(initialText)
        layout.addWidget(self.input)

        self.setLayout(layout)

    def GetInput(self):
        return self.input

    def GetValue(self):
        return self.input.text()


class Input2(QWidget):
    def __init__(
        self, label, initialText1, initialText2, labelWidth=None, *args, **kwargs
    ):
        super(Input2, self).__init__(*args, **kwargs)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(label)
        if labelWidth:
            self.label.setFixedWidth(labelWidth)
        layout.addWidget(self.label)

        self.input1 = QLineEdit(initialText1)
        layout.addWidget(self.input1)

        self.input2 = QLineEdit(initialText2)
        layout.addWidget(self.input2)

        self.setLayout(layout)

    def GetInput1(self):
        return self.input1

    def GetInput2(self):
        return self.input2


class InputNumber(QWidget):
    def __init__(self, label, initialNumber, labelWidth=None, *args, **kwargs):
        super(InputNumber, self).__init__(*args, **kwargs)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(label)
        if labelWidth:
            self.label.setFixedWidth(labelWidth)
        layout.addWidget(self.label)

        self.input = QSpinBox()
        self.input.setValue(initialNumber)
        layout.addWidget(self.input)

        self.setLayout(layout)

    def GetInput(self):
        return self.input
