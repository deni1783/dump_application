from functools import partial
from PyQt5 import QtWidgets, QtCore

from modules.my_classes import custom_functions

from modules.my_classes.SettingsWindow.ConnectionSettingsLayout import ConnectionSettings
from modules.my_classes.SettingsWindow.DumpSettingsLayout import DumpSettings

from modules.my_classes.ObjectsTreeWindow.ObjectTreeLayout import ObjectTree

from modules.Run_dump_dialects.postgresql import run_dump

from modules.queries_for_dialects import postgresql_home as postgresql

class Settings(ConnectionSettings, DumpSettings, ObjectTree):
    def __init__(self, parent=None):
        ConnectionSettings.__init__(self, parent)
        DumpSettings.__init__(self, parent)
        ObjectTree.__init__(self, parent)

        self.dialect_name = 'postgresql'

        self.settings = self.full_json_data[self.dialect_name]


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

        # Проверка соединения
        self.btn_test_connect.clicked.connect(partial(self.test_connection, postgresql.connect))

        # Обработчики для кнопок выбора баз данных
        # self.btn_default_databases.clicked.connect(partial(self.selected_default_databases))
        # self.btn_custom_databases.clicked.connect(partial(self.selected_custom_databases))


        # Обработчики для дерева объектов
        self.tree_widget.itemDoubleClicked.connect(partial(self.load_child_for_item,
                                                           postgresql.all_databases,
                                                           postgresql.all_schemas,
                                                           postgresql.all_tables))

        # self.tree_widget.itemChanged.connect(partial(self.click_flags))

        # Запуск дампа
        self.btn_run_creating_dump.clicked.connect(partial(self.run_creating_dump))




        # Возвращаемая обертка
        wrap_vbox = QtWidgets.QVBoxLayout()
        wrap_vbox.addWidget(self.box_conn_settings)
        wrap_vbox.addWidget(self.box_type_dump)


        wrap_full = QtWidgets.QHBoxLayout()
        wrap_full.addLayout(wrap_vbox)
        wrap_full.addWidget(self.box_object_tree)

        # Возвращаем в основной макет
        self.out_window = wrap_full


    def selected_default_databases(self):
        # Находим выбранный тип дампа
        checked_radio = self.get_selected_type_of_dump()
        print('Default DB', checked_radio.text())


    def selected_custom_databases(self):

        # Изменяем курсор в песочные часы
        custom_functions.set_cursor_style('wait')

        # Проверяем подключение если ошибка, выводим сообщение об ошибке
        status = self.test_connection(postgresql.connect)
        if status != 'Connected':
            return

        # Находим выбранный тип дампа
        checked_radio = self.get_selected_type_of_dump()

        print('Custom DB ', checked_radio.text())

        # Возвращаем обычный курсор
        custom_functions.set_cursor_style('normal')


    def run_creating_dump(self):
        if not self.lbl_selected_out_dir.text():
            error_msg = QtWidgets.QErrorMessage(self.box_conn_settings)
            error_msg.setWindowTitle('Not selected directory')
            error_msg.showMessage('Please select output directory and then try again')
            error_msg.show()
            return

        selected_items = self.get_checked_items_from_tree()
        # print(selected_items)
        # print(self.get_list_of_chacked_items(selected_items))

        current_connecting_settings = self.settings[self.combo_box_list_profiles.currentText()]
        list_of_selected_items = self.get_list_of_chacked_items(selected_items)
        checked_radio = self.get_selected_type_of_dump().text()
        run_dump(current_connecting_settings, 'path/to/pgdump.exe',
                 list_of_selected_items, checked_radio, 'path/to/output/dir')


    # def click_flags(self):
    #     current_item = self.tree_widget.currentItem()
    #     print('hi', current_item)