from PyQt5 import QtWidgets, QtCore
from modules.Layouts.PartsForSettingsWindow import ConnectionSettingsLayout, DumpSettingsLayout, ObjectTreeLayout


class GroupAllSettings(ConnectionSettingsLayout.ConnectionSettings,
                       DumpSettingsLayout.DumpSettings,
                       ObjectTreeLayout.ObjectTree):
    def __init__(self, parent=None):
        ConnectionSettingsLayout.ConnectionSettings.__init__(self, parent)
        DumpSettingsLayout.DumpSettings.__init__(self, parent)
        ObjectTreeLayout.ObjectTree.__init__(self, parent)


        # Виджет для вывода лога
        self.txt_edit_output_log = QtWidgets.QTextEdit()

        vbox_connection_and_dump_settings = QtWidgets.QVBoxLayout()
        vbox_connection_and_dump_settings.addWidget(self.box_conn_settings)
        vbox_connection_and_dump_settings.addWidget(self.box_dump_settings)

        self.box_con_dump_settings = QtWidgets.QGroupBox()
        self.box_con_dump_settings.setLayout(vbox_connection_and_dump_settings)

        hbox_grouped_con_dump_tree_objects = QtWidgets.QHBoxLayout()
        hbox_grouped_con_dump_tree_objects.addWidget(self.box_con_dump_settings)
        hbox_grouped_con_dump_tree_objects.addWidget(self.box_object_tree)

        # out_window возвращается в интерфейс
        self.out_window = QtWidgets.QVBoxLayout()
        self.out_window.addLayout(hbox_grouped_con_dump_tree_objects)
        self.out_window.addWidget(self.txt_edit_output_log)






        # =================================================
        # Устанавливаем стили оформления виджетов
        # =================================================
        # self.box_conn_settings     - гр бокс настроек подключения
        # self.box_dump_settings     - гр бокс настроек дампа

        # self.box_con_dump_settings - гр бокс настроек подключения и дампа

        # self.box_object_tree       - гр бокс настроек дерева
        # self.txt_edit_output_log   - виджет лога

        vbox_connection_and_dump_settings.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        hbox_grouped_con_dump_tree_objects.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.box_con_dump_settings.setFixedWidth(350)
        self.box_con_dump_settings.setFlat(True)



        # виджет лога
        self.txt_edit_output_log.setText('Output...')
        self.txt_edit_output_log.setStyleSheet("color: #777777")
        self.txt_edit_output_log.setReadOnly(True)
        self.txt_edit_output_log.setMaximumHeight(100)


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