from PyQt5 import QtWidgets
from functools import partial
from Modules.my_classes import custom_functions
import settings.Constants as CONST

# Новые диалекты добавляем в импорт
from Modules.Dialect.UI_window import (
    oracle, ms_sql_server, redshift, sybase, mysql, db2, teradata,
    greenplum, netezza, postgresql
)


class MainLayout(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # Получаем список всех диалектов
        list_dialects = custom_functions.get_all_dialects_from_json(CONST.PATH_TO_DIALECT_JSON)

        # Объект хранит { имя диалекта: кнопка }
        self.dialects_and_btn_obj = {}
        self.dialects_window_vbox = QtWidgets.QVBoxLayout()
        for i in list_dialects:
            self.dialects_and_btn_obj[i] = QtWidgets.QPushButton(i)
            self.dialects_window_vbox.addWidget(self.dialects_and_btn_obj[i])

        # Назначаем обработчики для кнопок.
        # При нажатии заполняется self.settings_layout
        for key in self.dialects_and_btn_obj:
            self.dialects_and_btn_obj[key].clicked.connect(partial(self.change_layout_for_dialect, key))

        # Окно настроек
        self.settings_layout = QtWidgets.QVBoxLayout()
        self.settings_window_gbox = QtWidgets.QGroupBox()
        self.settings_window_gbox.setLayout(self.settings_layout)

        # Добавляем группированные боксы в главное окно
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.dialects_window_vbox)
        self.main_layout.addWidget(self.settings_window_gbox)

        self.setLayout(self.main_layout)


    # Функция возвращает нужный виджет (QVBoxLayout) в зависимости от диалекта
    @staticmethod
    def return_current_vbox(dialect_name: str):
        if dialect_name.lower() == 'oracle':
            wrap_vbox = oracle.Settings().out_window
        elif dialect_name.lower() == 'ms sql server':
            wrap_vbox = ms_sql_server.Settings().out_window
        elif dialect_name.lower() == 'redshift':
            wrap_vbox = redshift.Settings().out_window
        elif dialect_name.lower() == 'sybase':
            wrap_vbox = sybase.Settings().out_window
        elif dialect_name.lower() == 'mysql':
            wrap_vbox = mysql.Settings().out_window
        elif dialect_name.lower() == 'db2':
            wrap_vbox = db2.Settings().out_window
        elif dialect_name.lower() == 'teradata':
            wrap_vbox = teradata.Settings().out_window
        elif dialect_name.lower() == 'postgresql':
            wrap_vbox = postgresql.Settings().out_window
        elif dialect_name.lower() == 'greenplum':
            wrap_vbox = greenplum.Settings().out_window
        elif dialect_name.lower() == 'netezza':
            wrap_vbox = netezza.Settings().out_window

        #  Если нет класса дня диалекта возвращаем пустую обертку
        else:
            wrap_vbox = QtWidgets.QVBoxLayout()
            err_lbl = QtWidgets.QLabel('Unsupported dialect: ' + dialect_name)
            wrap_vbox.addWidget(err_lbl)
        return wrap_vbox

    # Добавляет нужный виджет диалекта в интерфейс
    def change_layout_for_dialect(self, dialect):

        # Делаем все кнопки диалектов активными
        for btn in self.dialects_and_btn_obj:
            self.dialects_and_btn_obj[btn].setDisabled(False)
        # Устанавливаем кнопку выбраннокго диалекта неактивной
        self.dialects_and_btn_obj[dialect].setDisabled(True)

        self.settings_window_gbox.setTitle(dialect)

        # Полностью очищаем окно настроек
        custom_functions.clear_widget(self.settings_layout)

        # Заполняем окно настроек
        add_wgt = self.return_current_vbox(dialect)
        self.settings_layout.addLayout(add_wgt)
