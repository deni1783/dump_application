from PyQt5 import QtWidgets, QtCore


class WindowSettings(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.initUI()

    def initUI(self):


        # Разметка для настроек
        self.settings_grid = QtWidgets.QGridLayout()


        # Создание надписей
        self.host = QtWidgets.QLabel('HOST:')
        self.host_value = QtWidgets.QLabel('undefined')

        self.port = QtWidgets.QLabel('PORT:')
        self.port_value = QtWidgets.QLabel('undefined')

        self.user = QtWidgets.QLabel('USER:')
        self.user_value = QtWidgets.QLabel('undefined')

        self.password = QtWidgets.QLabel('PASSWORD:')
        self.password_value = QtWidgets.QLabel('undefined')

        self.database = QtWidgets.QLabel('DATABASE:')
        self.database_value = QtWidgets.QLabel('undefined')


        # Добавляем надписи в разметку
        self.settings_grid.addWidget(self.host, 0, 0)
        self.settings_grid.addWidget(self.host_value, 0, 1)

        self.settings_grid.addWidget(self.port, 1, 0)
        self.settings_grid.addWidget(self.port_value, 1, 1)

        self.settings_grid.addWidget(self.user, 2, 0)
        self.settings_grid.addWidget(self.user_value, 2, 1)

        self.settings_grid.addWidget(self.password, 3, 0)
        self.settings_grid.addWidget(self.password_value, 3, 1)

        self.settings_grid.addWidget(self.database, 4, 0)
        self.settings_grid.addWidget(self.database_value, 4, 1)

        # Группа настроек
        self.box_conn_settings = QtWidgets.QGroupBox('Connection settings')
        self.box_conn_settings.setAlignment(QtCore.Qt.AlignHCenter)
        self.box_conn_settings.setLayout(self.settings_grid)


        self.box_type_dump = QtWidgets.QGroupBox('Type of the dump')
        self.box_type_dump.setAlignment(QtCore.Qt.AlignHCenter)
