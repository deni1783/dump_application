from PyQt5 import QtWidgets, QtCore



class DumpSettings(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # Группа выбора тыпа дампа
        self.box_type_dump = QtWidgets.QGroupBox('Settings for DUMP')
        self.box_type_dump.setAlignment(QtCore.Qt.AlignHCenter)
