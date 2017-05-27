from PyQt5 import QtWidgets


class Settings(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.initUI()

    def initUI(self):

        vbox = QtWidgets.QVBoxLayout()


        wrap_vbox = QtWidgets.QVBoxLayout()
        lbl = QtWidgets.QLabel('test lbl for db2')
        wrap_vbox.addWidget(lbl)




        # Возвращаем в основной макет
        self.out_window = wrap_vbox



