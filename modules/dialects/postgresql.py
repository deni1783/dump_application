from functools import partial
from PyQt5 import QtWidgets, QtCore

from modules.Layouts.PartsForSettingsWindow.GroupedLayouts import GroupAllSettings

from modules.Run_dump_dialects.postgresql import get_list_of_cmd
from modules.my_classes import custom_functions
from modules.my_classes.MyThread import MyThread
from modules.queries_for_dialects import dummy_queries as postgresql
# from modules.queries_for_dialects import postgresql  # Изменить на нужный модуль


class Settings(GroupAllSettings):
    def __init__(self, parent=None):
        GroupAllSettings.__init__(self, parent)

        # ===============================================
        # Изменяемые параметры
        # \/ ========================================= \/


        # Обязательно устанавливаем название диалекта
        self.dialect_name = 'postgresql'

        # Устанавливаем тип элемента верхнего уровня в дереве объектов
        # self.top_level_item_type.setText(0, "Database")  # по-умолчанию
        # self.top_level_item_type.setText(0, "Schema")


        # Устанавливаем необходимые функции для работы с базой
        query_test_connection = postgresql.connect
        query_load_databases = postgresql.all_databases
        query_load_schemes = postgresql.all_schemas
        query_load_tables = postgresql.all_tables


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

        # Обработчики для кнопок выбора баз данных
        # self.btn_default_databases.clicked.connect(partial(self.selected_default_databases))
        # self.btn_custom_databases.clicked.connect(partial(self.selected_custom_databases))


        # Обработчики для дерева объектов
        self.tree_widget.itemDoubleClicked.connect(partial(self.load_children_for_parent,
                                                           query_load_databases,
                                                           query_load_schemes,
                                                           query_load_tables))


        # Запуск дампа
        self.btn_run_creating_dump.clicked.connect(partial(self.run_creating_dump))



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
        if not self.line_edit_selected_out_dir.text():
            error_msg = QtWidgets.QErrorMessage(self.box_conn_settings)
            error_msg.setWindowTitle('Not selected directory')
            error_msg.showMessage('Please select output directory and then try again')
            error_msg.show()
            return

        custom_functions.set_cursor_style('wait')
        self.btn_run_creating_dump.setDisabled(True)
        selected_items = self.get_checked_items_from_tree()

        current_connecting_settings = self.settings[self.combo_box_list_profiles.currentText()]
        list_of_selected_items = self.get_list_of_chacked_items(selected_items)
        checked_radio = self.get_selected_type_of_dump().text()
        list_of_cmd = get_list_of_cmd(self.dialect_name, current_connecting_settings, r'c:\program files\postgresql\9.5\bin\pg_dump.exe',
                                      list_of_selected_items, checked_radio, self.line_edit_selected_out_dir.text())

        self.mythread = MyThread(self.dialect_name, list_of_cmd)
        self.mythread.mysignal.connect(self.on_change_thread, QtCore.Qt.QueuedConnection)
        self.mythread.finished.connect(self.finish_thread)

        self.start_thread()

        # self.btn_run_creating_dump.setDisabled(False)
        custom_functions.set_cursor_style('normal')

    # def run_dump(self, connection_settings: dict,
    #              path_to_pgdump: str,
    #              objects: list,
    #              type_dump: str,
    #              out_dir: str):
    #     """
    #
    #     :param connection_settings: Объект с парамметрами подключения
    #     :param path_to_pgdump: Абсолютный путь к pgdump.exe
    #     :param objects: Массив объектов для которых необходимо сделать ДАМП
    #             [database1.schema1.table1, database3.schema1.table5]
    #     :param type_dump: Строковое значение типа дампа "Only Data, Only Schema, Data and Schema"
    #     :param out_dir: Абсолютный путь к папке, в которую выгружаем файлы ДАМПов
    #     :return: Запускает создание дампов, используются функции: run_cmd, write_to_log
    #     """
    #
    #     """
    #         default port is 5432
    #
    #
    #         "%pgdump$cmd%"
    #         - h % Server$name %
    #         -U % User$name %
    #         -p % Port$number %
    #         -d % Database %
    #         -n % Scheme$name %
    #         -t table_name
    #         % Type %
    #         -f % dir % % Scheme$name %.sql
    #
    #         Второй вариант:
    #
    #         "c:\program files\postgresql\9.5\bin\pg_dump.exe"
    #         -h"VM-DBA-2008R2-5"
    #         -U"qa"
    #         -p5432
    #         -s
    #         -f"D:\data\from_dump\gp_approxima.sql"
    #         -t"\"DBCS_D_GREENPLUM\".approximatenumerics" "DBCS_D_GREENPLUM"
    #     """
    #
    #     host = ' -h' + custom_functions.wrap_double_quotes(connection_settings['host'])
    #     user = ' -U' + custom_functions.wrap_double_quotes(connection_settings['user'])
    #     if connection_settings['port'] == 'default':
    #         port = ' -p' + '5432'
    #     else:
    #         port = ' -p' + connection_settings['port']
    #
    #     if type_dump == 'Only Data':
    #         type_d = '-a'
    #     elif type_dump == 'Only Schema':
    #         type_d = '-s'
    #     else:
    #         type_d = ''
    #
    #     list_of_cmd = []
    #
    #     for obj in objects:
    #         self.full_obj = obj
    #         tmp = obj.split('.')
    #         database = tmp[0]
    #         schema = tmp[1]
    #         table = tmp[2]
    #         normalize_outdir_path = os.path.normcase(out_dir + '/' + self.dialect_name + '/' + database + '/' + schema)
    #
    #         # Если папки нет, создаем
    #         # Папка диалекта
    #         if not os.path.isdir(os.path.normcase(out_dir + '/' + self.dialect_name)):
    #             os.mkdir(os.path.normcase(out_dir + '/' + self.dialect_name))
    #         # Папка базы
    #         if not os.path.isdir(os.path.normcase(out_dir + '/' + self.dialect_name + '/' + database)):
    #             os.mkdir(os.path.normcase(out_dir + '/' + self.dialect_name + '/' + database))
    #         # Папка схемы
    #         if not os.path.isdir(os.path.normcase(out_dir + '/' + self.dialect_name + '/' + database + '/' + schema)):
    #             os.mkdir(os.path.normcase(out_dir + '/' + self.dialect_name + '/' + database + '/' + schema))
    #
    #         out_file = normalize_outdir_path + '/' + table + '.sql'
    #         cmd_for_run = (custom_functions.wrap_double_quotes(path_to_pgdump) +
    #                        host +
    #                        user +
    #                        port +
    #                        ' ' + type_d +
    #                        ' -f' + custom_functions.wrap_double_quotes(out_file) +
    #                        ' -t' + '"' +
    #                        r'\"' + schema + r'\"' + '.' +
    #                        r'\"' + table + r'\"' +
    #                        '"' +
    #                        ' ' + '"' + database + '"'
    #                        )
    #
    #         list_of_cmd.append([obj, cmd_for_run])
    #
    #     self.mythread = MyThread(self.dialect_name, list_of_cmd)
    #     self.mythread.mysignal.connect(self.on_change_thread, QtCore.Qt.QueuedConnection)
    #     self.mythread.finished.connect(self.finish_thread)
    #
    #     self.start_thread()

    def start_thread(self):
        self.btn_run_creating_dump.setDisabled(True)
        self.mythread.start()

    def on_change_thread(self, object, code):
        if code == '0':
            status = 'Success'
        else:
            status = 'Error with code: ' + code
        self.txt_edit_output_log.append('Table ' + object + '\t Status: ' + status)
        # self.log_stat.setText(object + ' status code: ' + code)

    def finish_thread(self):
        self.btn_run_creating_dump.setDisabled(False)
