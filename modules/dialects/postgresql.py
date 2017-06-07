import os
from functools import partial

from PyQt5 import QtWidgets, QtCore

from modules.my_classes import custom_functions
from modules.my_classes.ClassForCMD.for_cmd import run_cmd
from modules.my_classes.ObjectsTreeWindow.ObjectTreeLayout import ObjectTree
from modules.my_classes.SettingsWindow.ConnectionSettingsLayout import ConnectionSettings
from modules.my_classes.SettingsWindow.DumpSettingsLayout import DumpSettings
from modules.my_classes.custom_functions import set_cursor_style
from modules.my_classes.custom_functions import wrap_double_quotes as wrap
from modules.my_classes.custom_functions import write_to_log
from modules.queries_for_dialects import postgresql_home as postgresql


# from modules.queries_for_dialects import postgresql as postgresql

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

        set_cursor_style('wait')
        self.btn_run_creating_dump.setDisabled(True)
        selected_items = self.get_checked_items_from_tree()
        # print(selected_items)
        # print(self.get_list_of_chacked_items(selected_items))

        current_connecting_settings = self.settings[self.combo_box_list_profiles.currentText()]
        list_of_selected_items = self.get_list_of_chacked_items(selected_items)
        checked_radio = self.get_selected_type_of_dump().text()
        self.run_dump(current_connecting_settings, 'path/to/pgdump.exe',
                 list_of_selected_items, checked_radio, 'path/to/output/dir')

        # self.btn_run_creating_dump.setDisabled(False)
        set_cursor_style('normal')


    def run_dump(self, connection_settings: dict, path_to_pgdump: str, objects: list, type_dump: str, out_dir: str):
        """

        :param connection_settings: Объект с парамметрами подключения
        :param path_to_pgdump: Абсолютный путь к pgdump.exe
        :param objects: Массив объектов для которых необходимо сделать ДАМП
                [database1.schema1.table1, database3.schema1.table5]
        :param type_dump: Строковое значение типа дампа "Only Data, Only Schema, Data and Schema"
        :param out_dir: Абсолютный путь к папке, в которую выгружаем файлы ДАМПов
        :return: Запускает создание дампов, используются функции: run_cmd, write_to_log
        """

        """
            default port is 5432


            "%pgdump$cmd%"
            - h % Server$name %
            -U % User$name %
            -p % Port$number %
            -d % Database %
            -n % Scheme$name %
            -t table_name
            % Type %
            -f % dir % % Scheme$name %.sql
        """

        dialect = self.dialect_name
        host = ' -h' + wrap(connection_settings['host'])
        user = ' -U' + wrap(connection_settings['user'])
        if connection_settings['port'] == 'default':
            port = ' -p' + '5432'
        else:
            port = ' -p' + connection_settings['port']

        if type_dump == 'Only Data':
            type_d = '-a'
        elif type_dump == 'Only Schema':
            type_d = '-s'
        else:
            type_d = ''

        list_of_cmd = []

        for obj in objects:
            self.full_obj = obj
            tmp = obj.split('.')
            database = ' -d' + wrap(tmp[0])
            schema = ' -n' + wrap(tmp[1])
            table = ' -t' + wrap(tmp[2])
            normalize_path = os.path.normcase(out_dir + '/' + tmp[0] + '/' + tmp[1] + tmp[2])
            out_file = ' -f' + wrap(normalize_path + '.sql')
            cmd_for_run = (wrap(path_to_pgdump) + host + user + port
                           + database + schema + table + ' ' + type_d
                           + out_file)

            list_of_cmd.append([obj, cmd_for_run])

        self.mythread = MyThread(list_of_cmd)
        self.mythread.mysignal.connect(self.on_change_thread, QtCore.Qt.QueuedConnection)
        self.mythread.finished.connect(self.finish_thread)

        self.start_thread()

            # self.mythread.start()

            # (code, stdout, stderr) = run_cmd(cmd_for_run)
            # write_to_log(dialect, obj, stdout, code, stderr)





    def start_thread(self):
        self.btn_run_creating_dump.setDisabled(True)
        self.mythread.start()

    def on_change_thread(self, object, code):
        self.log_stat.setText(object + ' status code: ' + code)

    def finish_thread(self):
        write_to_log(self.dialect_name, self.mythread.object,
                     self.mythread.stdout, self.mythread.code,
                     self.mythread.stderr)
        self.btn_run_creating_dump.setDisabled(False)


class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str, str)

    def __init__(self, list_of_cmd, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.list_cmd = list_of_cmd
        self.cmd = None
        self.code = None
        self.stdout = None
        self.stderr = None
        self.object = None

    def run(self):
        for i in self.list_cmd:
            self.sleep(2)
            self.object = i[0]
            self.cmd = i[1]
            print(self.cmd)
            (self.code, self.stdout, self.stderr) = run_cmd(self.cmd)
            self.mysignal.emit(self.object, str(self.code))




