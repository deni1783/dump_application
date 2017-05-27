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

        self.btn_save_profile.clicked.connect(partial(self.save_new_profile))


        # Возвращаемая обертка
        wrap_vbox = QtWidgets.QVBoxLayout()
        wrap_vbox.addWidget(self.box_conn_settings)
        wrap_vbox.addWidget(self.box_type_dump)


        # Возвращаем в основной макет
        self.out_window = wrap_vbox



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
        new_profile_name = self.line_new_profile_name_value.text()
        new_host = self.line_host_value.text()
        new_port = self.line_port_value.text()
        new_user = self.line_user_value.text()
        new_password = self.line_password_value.text()
        new_database = self.line_database_value.text()

        print(new_profile_name
                , new_host
                , new_port
                , new_user
                , new_password
                , new_database)
