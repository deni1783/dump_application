from PyQt5 import QtWidgets, QtCore
from modules.my_classes.WindowSettings import WindowSettings
from functools import partial


class Settings(WindowSettings):
    def __init__(self, parent=None):
        WindowSettings.__init__(self, parent)

        dialect = 'postgresql'

        self.settings = self.json_data[dialect]


        # =================================================
        # Настройка профилей
        # =================================================

        # Получаем список сохраненних профилей из настроек
        list_profiles = []
        for prof in self.settings:
            list_profiles.append(prof)

        # Заполняем список доступными профилями
        self.combo_box_list_profiles.addItems(list_profiles)


        # Получаем изначально активированный профиль
        activated_profile = self.combo_box_list_profiles.currentText()

        # Устанавливаем значения профиля
        profile = self.settings[activated_profile]

        # изменяем значения настроек подключения
        self.change_settings_values(profile)



        # =================================================
        # Устанавливае обработчики на кнопки
        # =================================================


        # Устанавливае обработчики на кнопки управления настройками
        self.btn_add_profile.clicked.connect(partial(self.add_profile))
        self.btn_change_settings.clicked.connect(partial(self.change_profile_settings))
        self.btn_test_connect.clicked.connect(partial(self.test_btn_clicked, 'test'))

        self.combo_box_list_profiles.activated[str].connect(partial(self.change_profile))

        # self.btn_save_profile.clicked.connect(partial(self.save_new_profile))


        # Возвращаемая обертка
        wrap_vbox = QtWidgets.QVBoxLayout()
        wrap_vbox.addWidget(self.box_conn_settings)
        wrap_vbox.addWidget(self.box_type_dump)


        # Возвращаем в основной макет
        self.out_window = wrap_vbox


    def add_profile(self):

        # Создание виджетов

        lbl_new_profile_name = QtWidgets.QLabel('New profile name')
        self.line_new_profile_name_value = QtWidgets.QLineEdit()
        self.line_host_value = QtWidgets.QLineEdit()
        self.line_port_value = QtWidgets.QLineEdit()
        self.line_user_value = QtWidgets.QLineEdit()
        self.line_password_value = QtWidgets.QLineEdit()
        self.line_database_value = QtWidgets.QLineEdit()

        # Кнопка сохранить
        self.btn_save_profile = QtWidgets.QPushButton('Save and Exit')
        self.btn_save_profile.setFixedWidth(150)
        self.btn_save_profile.clicked.connect(partial(self.save_new_profile))


        # Создание и заполние представления
        profile_layout = QtWidgets.QGridLayout()
        profile_layout.setAlignment(QtCore.Qt.AlignTop)


        profile_layout.addWidget(lbl_new_profile_name, 0, 0)
        profile_layout.addWidget(self.line_new_profile_name_value, 0, 1)

        profile_layout.addWidget(self.host, 1, 0)
        profile_layout.addWidget(self.line_host_value, 1, 1)

        profile_layout.addWidget(self.port, 2, 0)
        profile_layout.addWidget(self.line_port_value, 2, 1)

        profile_layout.addWidget(self.user, 3, 0)
        profile_layout.addWidget(self.line_user_value, 3, 1)

        profile_layout.addWidget(self.password, 4, 0)
        profile_layout.addWidget(self.line_password_value, 4, 1)

        profile_layout.addWidget(self.database, 5, 0)
        profile_layout.addWidget(self.line_database_value, 5, 1)

        profile_layout.addWidget(self.btn_save_profile, 6, 0, 1, 0)


        self.add_profile_window = QtWidgets.QWidget(parent=self.box_conn_settings)
        self.add_profile_window.setWindowFlags(QtCore.Qt.Tool)
        self.add_profile_window.setWindowTitle('New profile')

        self.add_profile_window.setLayout(profile_layout)
        self.add_profile_window.setMinimumSize(200, 200)


        self.add_profile_window.show()

        print('add profile')

    def change_profile_settings(self):
        print('change settings')

    def test_btn_clicked(self, txt):
        print('test connection', txt)

    def change_profile(self, profile_name):
        # Получаем новые значения
        new_profile = self.settings[profile_name]

        # Заполняем новыми значениями
        self.change_settings_values(new_profile)

    def save_new_profile(self):
        print('clicked save')
