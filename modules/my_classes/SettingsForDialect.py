from PyQt5 import QtWidgets, QtCore
import json





class WindowSettings(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.path_to_json_connecting_settings = 'settings/connection_settings.json'

        # Получаем объект настроек
        self.json_data = self.pars_json(self.path_to_json_connecting_settings)

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

        # Создание кнопок управления настройками
        self.btn_add_profile = QtWidgets.QPushButton('Add')
        self.btn_change_settings = QtWidgets.QPushButton('Change')
        self.btn_test_connect = QtWidgets.QPushButton('Test')


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



        # Добавление кнопок управления настройками
        self.settings_grid.addWidget(self.btn_add_profile, 0, 2)
        self.settings_grid.addWidget(self.btn_change_settings, 1, 2)
        self.settings_grid.addWidget(self.btn_test_connect, 2, 2)


        # Группа настроек
        self.box_conn_settings = QtWidgets.QGroupBox('Connection settings')
        self.box_conn_settings.setAlignment(QtCore.Qt.AlignHCenter)
        self.box_conn_settings.setLayout(self.settings_grid)


        self.box_type_dump = QtWidgets.QGroupBox('Type of the dump')
        self.box_type_dump.setAlignment(QtCore.Qt.AlignHCenter)


    @staticmethod
    def pars_json(file):
        data = open(file).read()
        json_data = json.loads(data)
        return json_data

    def change_value(self, obj):
        self.host_value.setText(obj['host'])
        self.port_value.setText(obj['port'])
        self.user_value.setText(obj['user'])
        self.password_value.setText(obj['password'])
        self.database_value.setText(obj['database'])
