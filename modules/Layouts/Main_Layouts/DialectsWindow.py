from PyQt5 import QtWidgets, QtCore
import json
# from modules.my_classes.Button import Button

# Прочитать и вернуть массив списка диалектов
def get_all_dialects_from_json(json_file):
    dialects = []
    data = open(json_file).read()
    json_data = json.loads(data)

    for dt_name in json_data['List_of_dialects']:
        dialects.append(dt_name)

    return dialects



class DialectsLayout(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        json_file = 'settings/dialects.json'

        self.list_dialects = get_all_dialects_from_json(json_file)

        self.dialects_obj = {}
        vbox = QtWidgets.QVBoxLayout()
        for i in self.list_dialects:
            self.dialects_obj[i] = QtWidgets.QPushButton(i)
            vbox.addWidget(self.dialects_obj[i])
        out_box = QtWidgets.QGroupBox()

        out_box.setLayout(vbox)

        # Возвращаем в основной макет
        self.out_window = out_box



