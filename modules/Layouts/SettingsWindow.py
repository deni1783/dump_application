from PyQt5 import QtWidgets, QtCore

# Новые диалекты добавляем в импорт
from modules.dialects import (
    oracle, ms_sql_server, redshift, sybase, mysql, db2, teradata,
    postgresql, greenplum, netezza
)


class SettingsLayout(QtWidgets.QWidget):
    def __init__(self, dialect_name: str, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.initUI(dialect_name)

    def initUI(self, dialect_name: str):

        # Для каждого диалекта добавляем условия и соответствующие классы
        # в папку modules/dialects
        if dialect_name.lower() == 'oracle':
            wrap_vbox = oracle.Settings().out_window
        elif dialect_name.lower() == 'ms sql server':
            wrap_vbox = ms_sql_server.Settings().out_window
        elif dialect_name.lower() == 'redshift':
            wrap_vbox = redshift.Settings().out_window
        elif dialect_name.lower() == 'sybase':
            wrap_vbox = sybase.Settings().out_window
        elif dialect_name.lower() == 'mysql':
            wrap_vbox = mysql.Settings().out_window
        elif dialect_name.lower() == 'db2':
            wrap_vbox = db2.Settings().out_window
        elif dialect_name.lower() == 'teradata':
            wrap_vbox = teradata.Settings().out_window
        elif dialect_name.lower() == 'postgresql':
            wrap_vbox = postgresql.SettingsFull().out_window
        elif dialect_name.lower() == 'greenplum':
            wrap_vbox = greenplum.Settings().out_window
        elif dialect_name.lower() == 'netezza':
            wrap_vbox = netezza.Settings().out_window

        #     Если нет класса дня диалекта возвращаем пустую обертку
        else:
            wrap_vbox = QtWidgets.QVBoxLayout()
            err_lbl = QtWidgets.QLabel('Unsupported dialect: ' + dialect_name)
            wrap_vbox.addWidget(err_lbl)

        out_box = QtWidgets.QGroupBox()
        out_box.setFlat(True)
        out_box.setAlignment(QtCore.Qt.AlignHCenter)
        out_box.setLayout(wrap_vbox)


        # Возвращаем в основной макет
        self.out_window = out_box



