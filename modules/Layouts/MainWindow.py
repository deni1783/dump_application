from PyQt5 import QtWidgets
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
        dialect_box = DialectsLayout(self)

        # Назначаем обработчики для кнопок
        for key in dialect_box.dialects_obj:
            dialect_box.dialects_obj[key].clicked.connect(partial(self.on_clicked_btn, key))





        # Окно настроек
        self.settings_layout = QtWidgets.QVBoxLayout()
        self.settings_box = QtWidgets.QGroupBox()
        self.settings_box.setFlat(True)
        self.settings_box.setLayout(self.settings_layout)




        # Добавляем группированные боксы в главное окно
        self.main_layout = QtWidgets.QHBoxLayout()

        self.main_layout.addWidget(dialect_box.out_window)
        self.main_layout.addWidget(self.settings_box)

        self.setLayout(self.main_layout)


    def on_clicked_btn(self, dialect):
        # print('clicked ', dialect)

        clear_widget(self.settings_layout)
        add_wgt = SettingsLayout(dialect).out_window
        self.settings_layout.addWidget(add_wgt)
