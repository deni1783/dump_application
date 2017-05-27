from PyQt5 import QtWidgets, QtCore


class WindowSettings(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.initUI()

    def initUI(self):

        self.box_conn_settings = QtWidgets.QGroupBox('Connection settings')
        self.box_conn_settings.setAlignment(QtCore.Qt.AlignHCenter)


        self.box_type_dump = QtWidgets.QGroupBox('Type of the dump')
        self.box_type_dump.setAlignment(QtCore.Qt.AlignHCenter)
