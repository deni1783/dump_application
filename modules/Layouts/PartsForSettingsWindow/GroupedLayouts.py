from PyQt5 import QtWidgets
from modules.Layouts.PartsForSettingsWindow import ConnectionSettingsLayout, DumpSettingsLayout, ObjectTreeLayout


class GroupAllSettings(ConnectionSettingsLayout.ConnectionSettings,
                       DumpSettingsLayout.DumpSettings,
                       ObjectTreeLayout.ObjectTree):
    def __init__(self, parent=None):
        ConnectionSettingsLayout.ConnectionSettings.__init__(self, parent)
        DumpSettingsLayout.DumpSettings.__init__(self, parent)
        ObjectTreeLayout.ObjectTree.__init__(self, parent)


        # Виджет для вывода лога
        self.output_log = QtWidgets.QTextEdit()
        self.output_log.setText('Output...')
        self.output_log.setStyleSheet("color: #777777")
        self.output_log.setReadOnly(True)
        self.output_log.setMaximumHeight(100)

        wrap_vbox = QtWidgets.QVBoxLayout()
        wrap_vbox.addWidget(self.box_conn_settings)
        wrap_vbox.addWidget(self.box_dump_settings)

        wrap_settings_tree = QtWidgets.QHBoxLayout()
        wrap_settings_tree.addLayout(wrap_vbox)
        wrap_settings_tree.addWidget(self.box_object_tree)

        # out_window возвращается в интерфейс
        self.out_window = QtWidgets.QVBoxLayout()
        self.out_window.addLayout(wrap_settings_tree)
        self.out_window.addWidget(self.output_log)

    def prepare_settings_for_profile(self, dialect_name):
        # Получаем необходимые настройки
        self.settings = self.full_json_data[dialect_name]

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