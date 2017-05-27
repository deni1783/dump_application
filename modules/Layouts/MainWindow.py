from PyQt5 import QtWidgets, QtCore
from modules.Layouts.DialectsWindow import DialectsLayout
from modules.Layouts.SettingsWindow import SettingsLayout
from functools import partial

# Полность очищает виджет
def clear_widget(obj):
    for i in reversed(range(obj.count())):
        obj.itemAt(i).widget().setParent(None)


class MainLayout(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.initUI()

    def initUI(self):


        # Окно выбора диалектов
        self.dialect_box = DialectsLayout(self)

        # Назначаем обработчики для кнопок
        for key in self.dialect_box.dialects_obj:
            self.dialect_box.dialects_obj[key].clicked.connect(partial(self.on_clicked_btn, key))





        # Окно настроек
        self.settings_layout = QtWidgets.QVBoxLayout()

        # Первоначальный вид
        preview_lbl = QtWidgets.QLabel('Settings for Dialect')
        preview_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.settings_layout.addWidget(preview_lbl)

        self.settings_box = QtWidgets.QGroupBox()
        self.settings_box.setTitle('Settings')
        self.settings_box.setAlignment(QtCore.Qt.AlignHCenter)

        self.settings_box.setFlat(True)
        self.settings_box.setLayout(self.settings_layout)




        # Добавляем группированные боксы в главное окно
        self.main_layout = QtWidgets.QHBoxLayout()

        self.main_layout.addWidget(self.dialect_box.out_window)
        self.main_layout.addWidget(self.settings_box)

        self.setLayout(self.main_layout)


    def on_clicked_btn(self, dialect):
        # print('clicked ', dialect)

        # Делаем все кнопки диалектов активными
        for btn in self.dialect_box.dialects_obj:
            self.dialect_box.dialects_obj[btn].setDisabled(False)
        # Устанавливаем кнопку выбраннокго диалекта неактивной
        self.dialect_box.dialects_obj[dialect].setDisabled(True)

        self.settings_box.setTitle(dialect)

        clear_widget(self.settings_layout)
        add_wgt = SettingsLayout(dialect).out_window
        self.settings_layout.addWidget(add_wgt)
