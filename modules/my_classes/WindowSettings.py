from PyQt5 import QtWidgets, QtCore
import json



class WindowSettings(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.path_to_json_connecting_settings = 'settings/connection_settings.json'

        # Получаем объект настроек
        self.json_data = self.pars_json(self.path_to_json_connecting_settings)


        # Обертка для выбора профиля настроек
        self.lbl_profile = QtWidgets.QLabel('Selected profile is')
        self.combo_box_list_profiles = QtWidgets.QComboBox()
        self.combo_box_list_profiles.setFixedWidth(150)

        self.hbox_profile = QtWidgets.QHBoxLayout()
        self.hbox_profile.setAlignment(QtCore.Qt.AlignHCenter)
        self.hbox_profile.addWidget(self.lbl_profile)
        self.hbox_profile.addWidget(self.combo_box_list_profiles)



        # Обертка для настроек
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


        # Общая обертка с профилем и настройками подключения
        self.vbox_profile_plus_settings = QtWidgets.QVBoxLayout()
        self.vbox_profile_plus_settings.addLayout(self.hbox_profile)
        self.vbox_profile_plus_settings.addLayout(self.settings_grid)

        # Кнопки управления

        # Создание кнопок управления настройками
        self.btn_add_profile = QtWidgets.QPushButton('Add')
        self.btn_change_settings = QtWidgets.QPushButton('Change')
        self.btn_test_connect = QtWidgets.QPushButton('Test')

        # Изменение вида кнопок
        self.btn_add_profile.setFixedWidth(100)
        self.btn_change_settings.setFixedWidth(100)
        self.btn_test_connect.setFixedWidth(100)


        # Обертка для кнопок управления настройками
        self.vbox_btns_change_settings = QtWidgets.QVBoxLayout()
        self.vbox_btns_change_settings.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)

        self.vbox_btns_change_settings.addWidget(self.btn_add_profile)
        self.vbox_btns_change_settings.addWidget(self.btn_change_settings)
        self.vbox_btns_change_settings.addWidget(self.btn_test_connect)



        # Обертка для настроек подключения
        # включает отображение настроек и кнопок управления ими
        self.hbox_wrap_settings = QtWidgets.QHBoxLayout()
        self.hbox_wrap_settings.addLayout(self.vbox_profile_plus_settings)
        self.hbox_wrap_settings.addLayout(self.vbox_btns_change_settings)




        # Группа настроек
        self.box_conn_settings = QtWidgets.QGroupBox('Connection settings')
        self.box_conn_settings.setAlignment(QtCore.Qt.AlignHCenter)
        self.box_conn_settings.setLayout(self.hbox_wrap_settings)


        # Группа выбора тыпа дампа
        self.box_type_dump = QtWidgets.QGroupBox('Type of the dump')
        self.box_type_dump.setAlignment(QtCore.Qt.AlignHCenter)


    @staticmethod
    def pars_json(file):
        data = open(file).read()
        json_data = json.loads(data)
        return json_data

    def change_settings_values(self, obj):
        self.host_value.setText(obj['host'])
        self.port_value.setText(obj['port'])
        self.user_value.setText(obj['user'])
        self.password_value.setText(obj['password'])
        self.database_value.setText(obj['database'])
