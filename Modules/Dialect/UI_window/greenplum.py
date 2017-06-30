from functools import partial

from PyQt5 import QtWidgets, QtCore

# from Modules.Dialect.Queries import dummy_queries as postgresql
from Modules.Dialect.Queries import greenplum
from Modules.Layouts.PartsForSettingsWindow.GroupedLayouts import GroupAllSettings
from Modules.Run_dump_dialects.postgresql import get_list_of_cmd
from Modules.my_classes import custom_functions
from Modules.my_classes.MyThread import MyThread
from settings import Constants

class Settings(GroupAllSettings):
    def __init__(self, parent=None):
        GroupAllSettings.__init__(self, parent)

        # ===============================================
        # Изменяемые параметры
        # \/ ========================================= \/


        # Обязательно устанавливаем название диалекта
        self.dialect_name = 'greenplum'

        # Устанавливаем тип элемента верхнего уровня в дереве объектов
        self.top_level_item_type.setText(0, "Database")  # по-умолчанию
        # self.top_level_item_type.setText(0, "Schema")


        # Устанавливаем необходимые функции для работы с базой
        query_test_connection = greenplum.connect
        query_load_databases = greenplum.all_databases
        query_load_schemes = greenplum.all_schemas
        query_load_tables = greenplum.all_tables


        # /\ ========================================= /\
        # Изменяемые параметры
        # ===============================================



        # Заполняем параметры профилей
        self.prepare_settings_for_profile(self.dialect_name)

        # =================================================
        # Устанавливаем обработчики на кнопки
        # =================================================

        # Проверка соединения
        self.btn_test_connect.clicked.connect(partial(self.test_connection, query_test_connection))


        # Обработчики для дерева объектов
        self.tree_widget.itemDoubleClicked.connect(partial(self.load_children_for_parent,
                                                           query_load_databases,
                                                           query_load_schemes,
                                                           query_load_tables))


        # Запуск дампа
        self.btn_run_creating_dump.clicked.connect(partial(self.run_creating_dump))


    def run_creating_dump(self):
        if not self.line_edit_selected_out_dir.text():
            error_msg = QtWidgets.QErrorMessage(self.box_conn_settings)
            error_msg.setWindowTitle('Not selected directory')
            error_msg.showMessage('Please select output directory and then try again')
            error_msg.show()
            return

        custom_functions.set_cursor_style('wait')
        self.btn_run_creating_dump.setDisabled(True)
        selected_items = self.get_checked_items_from_tree(self.top_level_item_type.text(0))
        print(selected_items)

        # current_connecting_settings = self.settings[self.combo_box_list_profiles.currentText()]
        # list_of_selected_items = self.get_list_of_chacked_items(selected_items)
        # checked_radio = self.get_selected_type_of_dump().text()
        # list_of_cmd = get_list_of_cmd(self.dialect_name, current_connecting_settings,
        #                               list_of_selected_items, checked_radio, self.line_edit_selected_out_dir.text())
        #
        # self.mythread = MyThread(self.dialect_name, list_of_cmd)
        # self.mythread.mysignal.connect(self.on_change_thread, QtCore.Qt.QueuedConnection)
        # self.mythread.finished.connect(self.finish_thread)
        #
        # self.start_thread()
        #
        # # self.btn_run_creating_dump.setDisabled(False)
        # custom_functions.set_cursor_style('normal')

    def start_thread(self):
        self.btn_run_creating_dump.setDisabled(True)
        self.mythread.start()

    def on_change_thread(self, object, code):
        if code == '0':
            status = 'Success'
        else:
            status = 'Error with code: ' + code
        self.txt_edit_output_log.append('Table ' + object + '\t Status: ' + status)

    def finish_thread(self):
        self.btn_run_creating_dump.setDisabled(False)
