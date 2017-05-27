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
        self.initUI()

    def initUI(self):
        json_file = 'settings/dialects.json'

        list_dialects = get_all_dialects_from_json(json_file)

        self.dialects_obj = {}

        vbox = QtWidgets.QVBoxLayout()
        vbox.setAlignment(QtCore.Qt.AlignTop)
        for i in list_dialects:
            self.dialects_obj[i] = QtWidgets.QPushButton(i)
            vbox.addWidget(self.dialects_obj[i])

        out_box = QtWidgets.QGroupBox('Dialects')
        out_box.setAlignment(QtCore.Qt.AlignHCenter)
        out_box.setStyleSheet('QGroupBox {'
                              'font-size: 14px;'
                              'font-weight: bold;'
                              'padding-top: 30px;'
                              'margin-top:10px'
                              '}')
        out_box.setMaximumWidth(180)
        out_box.setLayout(vbox)

        # Возвращаем в основной макет
        self.out_window = out_box



