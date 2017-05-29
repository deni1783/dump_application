from functools import partial
from PyQt5 import QtWidgets

from modules.my_classes.SettingsWindow.ConnectionSettingsLayout import ConnectionSettings
from modules.my_classes.SettingsWindow.DumpSettingsLayout import DumpSettings

from modules.my_classes.ObjectsTreeWindow.ObjectTreeLayout import ObjectTree


from modules.queries_for_dialects import postgresql

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


        # Устанавливае обработчики на кнопки управления настройками
        self.btn_add_profile.clicked.connect(partial(self.add_profile))
        self.btn_change_settings.clicked.connect(partial(self.change_profile_settings))
        self.btn_test_connect.clicked.connect(partial(self.test_btn_clicked, 'test'))

        self.combo_box_list_profiles.activated[str].connect(partial(self.change_profile))

        self.btn_save_profile.clicked.connect(partial(self.save_new_profile))

        # Обработчики для кнопок выбора баз данных
        self.btn_default_databases.clicked.connect(partial(self.selected_default_databases))
        self.btn_custom_databases.clicked.connect(partial(self.selected_custom_databases))


        # Обработцики для дерева объектов
        self.tree_widget.itemDoubleClicked.connect(partial(self.load_child_for_item, postgresql.load_schemas, postgresql.all_tables))

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


    def selected_default_databases(self):
        checked_radio = None
        # Находим выбранный тип дампа
        for r in (self.radio_only_data_type, self.radio_only_schema_type, self.radio_both_type):
            if r.isChecked():
                checked_radio = r
                break
        print('Default DB', checked_radio.text())


    def selected_custom_databases(self):
        # Получаем текущие настройки подключения
        current_connecting_settings = self.settings[self.combo_box_list_profiles.currentText()]

        checked_radio = None
        # Находим выбранный тип дампа
        for r in (self.radio_only_data_type, self.radio_only_schema_type, self.radio_both_type):
            if r.isChecked():
                checked_radio = r
                break

        # Добавляем объекты в дерево
        # self.add_objects_to_tree(self.full_json_data)
        result_arr = postgresql.all_databases(current_connecting_settings)
        self.add_children_to_parent_item(result_arr, self.tree_widget)


        print('Custom DB ', checked_radio.text())


    # def load_child_for_item(self):
    #     print(self.tree_widget.currentItem().text(0))

    def run_creating_dump(self):
        # t = self.tree_widget.itemClicked()
        print(self.arr_of_selected_item_in_tree)

    def load_child_for_item(self, func_load_schemas=None, func_load_tables=None):
        current_connecting_settings = self.settings[self.combo_box_list_profiles.currentText()]
        # Тип элемента (база, схема, таблица)
        type_of_item = None

        current_item = self.tree_widget.currentItem()

        if current_item.parent():
            if current_item.parent().parent():
                if not current_item.parent().parent().parent():
                    type_of_item = 'table'
            else:
                type_of_item = 'schema'
        else:
            type_of_item = 'database'


        if type_of_item == 'table': return

        if type_of_item == 'database':
            current_connecting_settings["database"] = current_item.text(0)
            result_obj = func_load_schemas(current_connecting_settings, current_item.text(0))
            self.add_children_to_parent_item(result_obj, current_item)
            print(current_item.childCount())
