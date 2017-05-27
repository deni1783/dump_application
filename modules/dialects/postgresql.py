from PyQt5 import QtWidgets, QtCore
from modules.my_classes.WindowSettings import WindowSettings
from functools import partial


class Settings(WindowSettings):
    def __init__(self, parent=None):
        WindowSettings.__init__(self, parent)

        settings = self.json_data['postgresql']

        profile = settings['default']

        # изменяем значения настроек подключения
        self.change_value(profile)

        # Устанавливае обработчики на кнопки управления настройками
        self.btn_add_profile.clicked.connect(partial(self.add_profile))
        self.btn_change_settings.clicked.connect(partial(self.change_profile_settings))
        self.btn_test_connect.clicked.connect(partial(self.test_btn_clicked, 'test'))





        # Возвращаемая обертка
        wrap_vbox = QtWidgets.QVBoxLayout()
        wrap_vbox.addWidget(self.box_conn_settings)
        wrap_vbox.addWidget(self.box_type_dump)


        # Возвращаем в основной макет
        self.out_window = wrap_vbox


    def add_profile(self):
        print('add profile')

    def change_profile_settings(self):
        print('change settings')

    def test_btn_clicked(self, txt):
        print('test connection', txt)
