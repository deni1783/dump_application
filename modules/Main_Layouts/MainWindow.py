from PyQt5 import QtWidgets, QtCore

from modules.Main_Layouts.DialectsWindow import DialectsLayout
from modules.Main_Layouts.SettingsWindow import SettingsLayout

from modules.my_classes import custom_functions
from functools import partial


class MainLayout(QtWidgets.QWidget):
    # self.dialect_box.out_window   - окно списка диалектов
    # self.settings_box             - окно настроек и дерева для диалекта

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # Окно выбора диалектов
        self.dialect_box = DialectsLayout(self)

        # Окно настроек
        self.settings_layout = QtWidgets.QVBoxLayout()

        # Назначаем обработчики для кнопок
        for key in self.dialect_box.dialects_obj:
            self.dialect_box.dialects_obj[key].clicked.connect(partial(self.change_layout_for_dialect, key))


        # Первоначальный вид
        # preview_lbl = QtWidgets.QLabel('Settings for Dialect')
        # preview_lbl.setAlignment(QtCore.Qt.AlignCenter)
        # self.settings_layout.addWidget(preview_lbl)

        self.settings_box = QtWidgets.QGroupBox()
        # self.settings_box.setTitle('Settings')
        # self.settings_box.setAlignment(QtCore.Qt.AlignHCenter)

        # self.settings_box.setFlat(True)
        self.settings_box.setLayout(self.settings_layout)

        # Добавляем группированные боксы в главное окно
        self.main_layout = QtWidgets.QHBoxLayout()

        self.main_layout.addWidget(self.dialect_box.out_window)
        self.main_layout.addWidget(self.settings_box)

        self.setLayout(self.main_layout)


    # Добавляет нужный виджет диалекта в интерфейс
    def change_layout_for_dialect(self, dialect):

        # Делаем все кнопки диалектов активными
        for btn in self.dialect_box.dialects_obj:
            self.dialect_box.dialects_obj[btn].setDisabled(False)
        # Устанавливаем кнопку выбраннокго диалекта неактивной
        self.dialect_box.dialects_obj[dialect].setDisabled(True)

        self.settings_box.setTitle(dialect)

        custom_functions.clear_widget(self.settings_layout)
        add_wgt = SettingsLayout(dialect).out_window
        self.settings_layout.addWidget(add_wgt)
