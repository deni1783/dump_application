from PyQt5 import QtWidgets, QtCore
from modules.my_classes.WindowSettings import WindowSettings



class Settings(WindowSettings):
    def __init__(self, parent=None):
        WindowSettings.__init__(self, parent)

        settings = self.json_data['postgresql']

        profile = settings['default']

        # изменяем значения
        self.change_value(profile)





        # Возвращаемая обертка
        wrap_vbox = QtWidgets.QVBoxLayout()
        wrap_vbox.addWidget(self.box_conn_settings)
        wrap_vbox.addWidget(self.box_type_dump)


        # Возвращаем в основной макет
        self.out_window = wrap_vbox



