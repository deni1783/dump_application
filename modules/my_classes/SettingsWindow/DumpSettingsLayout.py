from PyQt5 import QtWidgets, QtCore



class DumpSettings(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # Обортка в которую добавляем виджеты она присваивается box_type_dump
        main_wrap_hbox = QtWidgets.QHBoxLayout()

        # Группа выбора типа дампа
        box_dump = QtWidgets.QGroupBox('Type of the dump')
        box_dump.setFlat(True)
        box_dump.setAlignment(QtCore.Qt.AlignHCenter)

        self.radio_only_data_type = QtWidgets.QRadioButton('Only Data')
        self.radio_only_schema_type = QtWidgets.QRadioButton('Only Schema')
        self.radio_only_schema_type.setChecked(True)
        self.radio_both_type = QtWidgets.QRadioButton('Data and Schema')

        type_dump_vbox = QtWidgets.QVBoxLayout()
        type_dump_vbox.setAlignment(QtCore.Qt.AlignTop)

        type_dump_vbox.addWidget(self.radio_only_data_type)
        type_dump_vbox.addWidget(self.radio_only_schema_type)
        type_dump_vbox.addWidget(self.radio_both_type)

        box_dump.setLayout(type_dump_vbox)


        # Группа выбора нужных баз данных
        box_database = QtWidgets.QGroupBox('Select databases')
        box_database.setFlat(True)

        box_database.setAlignment(QtCore.Qt.AlignHCenter)

        self.btn_default_databases = QtWidgets.QPushButton('Default')
        self.btn_custom_databases = QtWidgets.QPushButton('Custom')

        database_vbox = QtWidgets.QVBoxLayout()
        database_vbox.setAlignment(QtCore.Qt.AlignTop)

        database_vbox.addWidget(self.btn_default_databases)
        database_vbox.addWidget(self.btn_custom_databases)
        box_database.setLayout(database_vbox)



        # Добавляем виджеты на главный экран
        main_wrap_hbox.addWidget(box_dump)
        main_wrap_hbox.addWidget(box_database)


        # Группа выбора тыпа дампа
        # Этот виджет используется в Родительском классе!
        self.box_type_dump = QtWidgets.QGroupBox('Settings for DUMP')
        self.box_type_dump.setAlignment(QtCore.Qt.AlignHCenter)
        self.box_type_dump.setLayout(main_wrap_hbox)

        self.box_type_dump.setFixedHeight(150)
