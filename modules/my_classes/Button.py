from PyQt5 import QtWidgets


class Button(QtWidgets.QWidget):
    def __init__(self, dialect_name, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.btn = QtWidgets.QPushButton(dialect_name)
        self.btn.clicked.connect(lambda: self.on_clicked_btn(dialect_name))


    # def initUI(self, dialect_name):
    #     btn = QtWidgets.QPushButton(dialect_name)
    #     btn.clicked.connect(lambda: self.on_clicked_btn(dialect_name))


    def on_clicked_btn(self, dialect_name):
        print(dialect_name)
