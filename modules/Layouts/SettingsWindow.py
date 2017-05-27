from PyQt5 import QtWidgets, QtCore
from modules.dialects import postgresql, greenplum


class SettingsLayout(QtWidgets.QWidget):
    def __init__(self, dialect_name: str, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.initUI(dialect_name)

    def initUI(self, dialect_name: str):

        # Для каждого диалекта добавляем условия и соответствующие классы в папку modules/dialects
        if dialect_name.lower() == 'postgresql':
            wrap_vbox = postgresql.Settings().out_window
        elif dialect_name.lower() == 'greenplum':
            wrap_vbox = greenplum.Settings().out_window
        elif dialect_name.lower() == 'oracle':
            wrap_vbox = greenplum.Settings().out_window

        out_box = QtWidgets.QGroupBox(dialect_name)
        out_box.setAlignment(QtCore.Qt.AlignHCenter)
        out_box.setLayout(wrap_vbox)


        # Возвращаем в основной макет
        self.out_window = out_box



