from PyQt5 import QtWidgets, QtCore, QtGui

class DumpSettings(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)


        lbl_type_dump = QtWidgets.QLabel('Type of dump is:')

        self.radio_only_data_type = QtWidgets.QRadioButton('Only Data')
        self.radio_only_schema_type = QtWidgets.QRadioButton('Only Schema')
        self.radio_only_schema_type.setChecked(True)
        self.radio_both_type = QtWidgets.QRadioButton('Data and Schema')


        vbox_type_dump = QtWidgets.QVBoxLayout()
        vbox_type_dump.addWidget(self.radio_only_data_type)
        vbox_type_dump.addWidget(self.radio_only_schema_type)
        vbox_type_dump.addWidget(self.radio_both_type)

        hbox_type_dump = QtWidgets.QHBoxLayout()
        hbox_type_dump.addWidget(lbl_type_dump)
        hbox_type_dump.addLayout(vbox_type_dump)



        self.btn_select_out_dir = QtWidgets.QPushButton('Pick output dir')
        self.line_edit_selected_out_dir = QtWidgets.QLineEdit()
        self.line_edit_selected_out_dir.setReadOnly(True)

        # self.lbl_selected_out_dir.setLineWrapColumnOrWidth(200)
        # self.lbl_selected_out_dir.setLineWrapMode(QtWidgets.QTextEdit.FixedPixelWidth)
        # self.lbl_selected_out_dir.setWordWrapMode(QtGui.QTextOption.NoWrap)
        # self.text_edit_selected_out_dir.setFixedHeight(40)

        hbox_output_dir = QtWidgets.QHBoxLayout()
        hbox_output_dir.addWidget(self.btn_select_out_dir)
        hbox_output_dir.addWidget(self.line_edit_selected_out_dir)

        self.btn_default_databases = QtWidgets.QPushButton('Choice default list of database')
        self.btn_default_databases.setDisabled(True)

        """
        # Обортка в которую добавляем виджеты она присваивается box_type_dump
        main_wrap_hbox = QtWidgets.QHBoxLayout()

        # Группа выбора типа дампа
        box_dump = QtWidgets.QGroupBox('Type of the dump is')
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
        self.btn_default_databases.setDisabled(True)
        self.btn_custom_databases = QtWidgets.QPushButton('Custom')
        self.btn_custom_databases.setDisabled(True)

        database_vbox = QtWidgets.QVBoxLayout()
        database_vbox.setAlignment(QtCore.Qt.AlignTop)

        database_vbox.addWidget(self.btn_default_databases)
        database_vbox.addWidget(self.btn_custom_databases)
        box_database.setLayout(database_vbox)




        main_wrap_hbox.addWidget(box_dump)
        main_wrap_hbox.addWidget(box_database)


        # Выбор папки назначения для дампов
        lbl_select_dir = QtWidgets.QLabel('Please select output directory')
        self.btn_select_out_dir = QtWidgets.QPushButton('Directory')
        lbl_selected_dir_is = QtWidgets.QLabel('Selected directory is:')
        self.lbl_selected_out_dir = QtWidgets.QLabel()
        self.lbl_selected_out_dir.setStyleSheet('QLabel {color: green;}')
        self.btn_run_thread = QtWidgets.QPushButton('Run Thread')
        self.log_stat = QtWidgets.QLabel('Loging...')

        self.txt_log = QtWidgets.QTextEdit()
        self.txt_log.setReadOnly(True)


        hbox_select_dir = QtWidgets.QHBoxLayout()
        hbox_select_dir.addWidget(lbl_select_dir)
        hbox_select_dir.addWidget(self.btn_select_out_dir)

        vbox_wrap_select_dir = QtWidgets.QVBoxLayout()
        vbox_wrap_select_dir.addLayout(main_wrap_hbox)
        vbox_wrap_select_dir.addLayout(hbox_select_dir)
        vbox_wrap_select_dir.addWidget(lbl_selected_dir_is)
        vbox_wrap_select_dir.addWidget(self.lbl_selected_out_dir)
        vbox_wrap_select_dir.addWidget(self.btn_run_thread)
        vbox_wrap_select_dir.addWidget(self.log_stat)
        vbox_wrap_select_dir.addWidget(self.txt_log)



        """
        # Представление для добавления виджетов
        vbox_dump_settings = QtWidgets.QVBoxLayout()
        vbox_dump_settings.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        vbox_dump_settings.addLayout(hbox_type_dump)
        vbox_dump_settings.addLayout(hbox_output_dir)
        vbox_dump_settings.addWidget(self.btn_default_databases)

        # Группа выбора тыпа дампа
        # Этот виджет используется в Родительском классе!
        self.box_dump_settings = QtWidgets.QGroupBox('Settings for DUMP')
        self.box_dump_settings.setAlignment(QtCore.Qt.AlignHCenter)
        self.box_dump_settings.setLayout(vbox_dump_settings)

        # self.box_type_dump.setFixedHeight(150)

        # Обработчики для кнопок
        self.btn_select_out_dir.clicked.connect(self.select_folder)

    def select_folder(self):
        folder_name = QtWidgets.QFileDialog.getExistingDirectory(self, caption='Select folder')
        self.line_edit_selected_out_dir.setText(folder_name)

    def get_selected_type_of_dump(self):
        for r in (self.radio_only_data_type, self.radio_only_schema_type, self.radio_both_type):
            if r.isChecked():
                return r
