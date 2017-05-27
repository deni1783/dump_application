from PyQt5 import QtWidgets, QtCore
from modules.my_classes.SettingsForDialect import WindowSettings



class Settings(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.initUI()

    def initUI(self):


        main_box = WindowSettings()



        vbox = QtWidgets.QVBoxLayout()


        lbl = QtWidgets.QLabel('test lbl for postgresql')
        box = QtWidgets.QGroupBox('Connection settings')
        box.setAlignment(QtCore.Qt.AlignHCenter)

        vbox.addWidget(lbl)

        box.setLayout(vbox)

        # print(main_box.json_data)


        # Возвращаемая обертка
        wrap_vbox = QtWidgets.QVBoxLayout()
        wrap_vbox.addWidget(main_box.box_conn_settings)
        wrap_vbox.addWidget(main_box.box_type_dump)


        # Возвращаем в основной макет
        self.out_window = wrap_vbox



