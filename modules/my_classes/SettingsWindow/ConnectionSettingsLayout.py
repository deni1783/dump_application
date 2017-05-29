from PyQt5 import QtWidgets, QtCore
import json



class ConnectionSettings(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.dialect_name = None

        # Кнопка сохранить выбранных профиль
        self.btn_save_profile = QtWidgets.QPushButton('Save and Exit')
        # self.btn_save_profile.setFixedWidth(150)
        self.btn_save_profile.setDisabled(True)

        self.line_new_profile_name_value = QtWidgets.QLineEdit()
        self.line_new_profile_name_value.textChanged[str].connect(self.activate_save_profile_btn)
        self.line_host_value = QtWidgets.QLineEdit()
        self.line_host_value.textChanged[str].connect(self.activate_save_profile_btn)
        self.line_port_value = QtWidgets.QLineEdit()
        self.line_user_value = QtWidgets.QLineEdit()
        self.line_user_value.textChanged[str].connect(self.activate_save_profile_btn)
        self.line_password_value = QtWidgets.QLineEdit()
        self.line_database_value = QtWidgets.QLineEdit()

        self.path_to_json_connecting_settings = 'settings/connection_settings.json'

        # Получаем объект настроек
        self.full_json_data = self.pars_json(self.path_to_json_connecting_settings)


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



    @staticmethod
    def pars_json(file):
        data = open(file).read()
        json_data = json.loads(data)
        return json_data


    def write_obj_to_json_file(self, obj):
        json.dump(obj, open(self.path_to_json_connecting_settings, 'w'), indent=2)

    def change_settings_values(self, obj):
        self.host_value.setText(obj['host'])
        self.port_value.setText(obj['port'])
        self.user_value.setText(obj['user'])
        self.password_value.setText(obj['password'])
        self.database_value.setText(obj['database'])

    def add_profile(self):

        # Создание виджетов
        lbl_new_profile_name = QtWidgets.QLabel('New profile name')

        host = QtWidgets.QLabel('HOST:')
        port = QtWidgets.QLabel('PORT:')
        user = QtWidgets.QLabel('USER:')
        password = QtWidgets.QLabel('PASSWORD:')
        database = QtWidgets.QLabel('DATABASE:')

        # Создание и заполние представления
        self.profile_layout = QtWidgets.QGridLayout()
        self.profile_layout.setAlignment(QtCore.Qt.AlignTop)


        self.profile_layout.addWidget(lbl_new_profile_name, 0, 0)
        self.profile_layout.addWidget(self.line_new_profile_name_value, 0, 1)

        self.profile_layout.addWidget(host, 1, 0)
        self.profile_layout.addWidget(self.line_host_value, 1, 1)

        self.profile_layout.addWidget(port, 2, 0)
        self.profile_layout.addWidget(self.line_port_value, 2, 1)

        self.profile_layout.addWidget(user, 3, 0)
        self.profile_layout.addWidget(self.line_user_value, 3, 1)

        self.profile_layout.addWidget(password, 4, 0)
        self.profile_layout.addWidget(self.line_password_value, 4, 1)

        self.profile_layout.addWidget(database, 5, 0)
        self.profile_layout.addWidget(self.line_database_value, 5, 1)

        self.profile_layout.addWidget(self.btn_save_profile, 6, 0, 1, 0)


        self.add_profile_window = QtWidgets.QWidget(parent=self.box_conn_settings)
        self.add_profile_window.setWindowFlags(QtCore.Qt.Tool)
        self.add_profile_window.setWindowTitle('New profile')

        self.add_profile_window.setLayout(self.profile_layout)
        # self.add_profile_window.setMinimumSize(200, 200)

        # self.line_new_profile_name_value


        self.add_profile_window.show()

    def activate_save_profile_btn(self):
        if self.line_new_profile_name_value.text() and \
                self.line_host_value.text() and \
                self.line_user_value.text():
            self.btn_save_profile.setDisabled(False)
        else:
            self.btn_save_profile.setDisabled(True)

    def save_new_profile(self):
        new_profile_name = self.line_new_profile_name_value.text()
        new_host = self.line_host_value.text()
        new_port = self.line_port_value.text()
        new_user = self.line_user_value.text()
        new_password = self.line_password_value.text()
        new_database = self.line_database_value.text()

        self.full_json_data[self.dialect_name][new_profile_name] = {
            "host": new_host,
            "port": new_port,
            "user": new_user,
            "password": new_password,
            "database": new_database
        }
        self.write_obj_to_json_file(self.full_json_data)
        self.combo_box_list_profiles.addItem(new_profile_name)
        self.add_profile_window.close()
