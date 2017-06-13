from functools import partial
from PyQt5 import QtWidgets

from modules.Layouts.PartsForSettingsWindow.DumpSettingsLayout import DumpSettings
from modules.Layouts.PartsForSettingsWindow.ConnectionSettingsLayout import ConnectionSettings
from modules.Layouts.PartsForSettingsWindow.ObjectTreeLayout import ObjectTree

from modules.my_classes import custom_functions
from modules.queries_for_dialects import greenplum


class Settings(ConnectionSettings, DumpSettings, ObjectTree):
    def __init__(self, parent=None):
        ConnectionSettings.__init__(self, parent)
        DumpSettings.__init__(self, parent)
        ObjectTree.__init__(self, parent)

        self.dialect_name = 'greenplum'

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
        self.btn_test_connect.clicked.connect(partial(self.test_connection, greenplum.connect))

        # Обработчики для кнопок выбора баз данных
        self.btn_default_databases.clicked.connect(partial(self.selected_default_databases))
        # self.btn_custom_databases.clicked.connect(partial(self.selected_custom_databases))

        # Обработчики для дерева объектов
        self.tree_widget.itemDoubleClicked.connect(partial(self.load_children_for_parent,
                                                           greenplum.all_databases,
                                                           greenplum.all_schemas,
                                                           greenplum.all_tables))

        # self.tree_widget.itemChanged.connect(partial(self.click_flags))

        # Запуск дампа
        self.btn_run_creating_dump.clicked.connect(partial(self.run_creating_dump))

        # Возвращаемая обертка
        wrap_vbox = QtWidgets.QVBoxLayout()
        wrap_vbox.addWidget(self.box_conn_settings)
        wrap_vbox.addWidget(self.box_dump_settings)

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
        status = self.test_connection(greenplum.connect)
        if status != 'Connected':
            return

        # Находим выбранный тип дампа
        checked_radio = self.get_selected_type_of_dump()

        print('Custom DB ', checked_radio.text())

        # Возвращаем обычный курсор
        custom_functions.set_cursor_style('normal')

    def run_creating_dump(self):
        selected_items = self.get_checked_items_from_tree(self.tree_widget)
        print(selected_items)

    def click_flags(self):
        current_item = self.tree_widget.currentItem()
        print('hi', current_item)