from PyQt5 import QtWidgets, QtCore
from functools import partial


class ObjectTree(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.arr_of_selected_item_in_tree = []

        self.vbox_obj_tree = QtWidgets.QVBoxLayout()


        # Дерево выгруженных объектов
        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setHeaderLabel('Databases')
        self.tree_widget.setSortingEnabled(True)
        self.tree_widget.setAnimated(True)

        self.tree_widget.itemClicked.connect(partial(self.clicked_item))

        # Запуск дампа
        self.btn_run_creating_dump = QtWidgets.QPushButton('Run creating DUMP')
        # self.btn_run_creating_dump.clicked.connect(partial(self.run_creating_dump))

        self.vbox_obj_tree.addWidget(self.tree_widget)
        self.vbox_obj_tree.addWidget(self.btn_run_creating_dump)



        self.box_object_tree = QtWidgets.QGroupBox('Objects Tree')
        self.box_object_tree.setAlignment(QtCore.Qt.AlignHCenter)
        self.box_object_tree.setLayout(self.vbox_obj_tree)
        # self.box_object_tree.hide()

    def add_objects_to_tree(self, obj):

        for d in obj:
            database = QtWidgets.QTreeWidgetItem(self.tree_widget)
            database.setText(0, "{}".format(d))
            database.setFlags(database.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)

            for s in obj[d]:
                schema = QtWidgets.QTreeWidgetItem(database)
                schema.setText(0, "{}".format(s))
                schema.setFlags(schema.flags() | QtCore.Qt.ItemIsUserCheckable)
                schema.setCheckState(0, QtCore.Qt.Unchecked)

                for t in obj[d][s]:
                    table = QtWidgets.QTreeWidgetItem(schema)
                    table.setText(0, "{}".format(t))
                    table.setFlags(table.flags() | QtCore.Qt.ItemIsUserCheckable)
                    table.setCheckState(0, QtCore.Qt.Unchecked)

    # def run_creating_dump(self):
    #     print(self.tree_widget.currentItem())

    def clicked_item(self):
        current_item = self.tree_widget.currentItem()

        # Статус флага
        checked_status = current_item.checkState(0)
        if checked_status == 0:
            current_item.setCheckState(0, QtCore.Qt.Checked)
        else:
            current_item.setCheckState(0, QtCore.Qt.Unchecked)

        # Вычисляем родителей
        tmp_str = ''
        if current_item.parent():
            # Если есть и нет
            tmp_str += '.' + current_item.parent().text(0)
            if current_item.parent().parent():
                # Если есть то это база
                tmp_str = current_item.parent().parent().text(0) + '.' + tmp_str

        print(tmp_str, current_item.text(0))