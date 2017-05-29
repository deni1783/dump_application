from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial

def check_type_of_item(item):
    if item.parent():
        if item.parent().parent():
            if not item.parent().parent().parent():
                return 'table'
        else:
            return 'schema'
    else:
        return 'database'

class ObjectTree(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.dialect_name = None

        # Массив выбранных элементов из дерева для которых нужно выполнить дамп
        self.arr_of_selected_item_in_tree = []

        self.vbox_obj_tree = QtWidgets.QVBoxLayout()


        # Дерево выгруженных объектов
        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setMinimumWidth(300)
        self.tree_widget.setMinimumHeight(400)
        self.tree_widget.setHeaderLabel('Objects')
        self.tree_widget.setSortingEnabled(True)
        self.tree_widget.setAnimated(True)

        # self.tree_widget.itemClicked.connect(partial(self.clicked_item))
        # self.tree_widget.itemDoubleClicked.connect(partial(self.load_child_for_item))

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

        # Загружаем базы
        for d in obj:
            database = QtWidgets.QTreeWidgetItem(self.tree_widget)
            database.setText(0, "{}".format(d))
            database.setIcon(0, QtGui.QIcon("icons/database.png"))
            database.setFlags(database.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)

            # Загружаем схемы
            for s in obj[d]:
                schema = QtWidgets.QTreeWidgetItem(database)
                schema.setText(0, "{}".format(s))
                schema.setIcon(0, QtGui.QIcon("icons/schema.png"))
                schema.setFlags(schema.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
                schema.setCheckState(0, QtCore.Qt.Unchecked)

                # Загружаем таблицы
                for t in obj[d][s]:
                    table = QtWidgets.QTreeWidgetItem(schema)
                    table.setText(0, "{}".format(t))
                    table.setIcon(0, QtGui.QIcon("icons/table.png"))
                    table.setFlags(table.flags() | QtCore.Qt.ItemIsUserCheckable)
                    table.setCheckState(0, QtCore.Qt.Unchecked)


    def add_children_to_parent_item(self, child_arr, parent):
        for item in child_arr:
            child = QtWidgets.QTreeWidgetItem(parent)
            child.setText(0, "{}".format(item))
            child.setIcon(0, QtGui.QIcon("icons/database.png"))
            child.setFlags(child.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
            child.setCheckState(0, QtCore.Qt.Unchecked)

    def clicked_item(self):
        current_item = self.tree_widget.currentItem()

        # Статус флага (0 - не выбран, 2 - выбран)
        checked_status = current_item.checkState(0)
        if checked_status == 0:
            current_item.setCheckState(0, QtCore.Qt.Checked)
        else:
            current_item.setCheckState(0, QtCore.Qt.Unchecked)

        # Вычисляем родителей
        tmp_str = ''
        if current_item.parent():
            # Если есть то либо схема, либо база
            tmp_str += current_item.parent().text(0) + '.'
            if current_item.parent().parent():
                # Если есть то это точно база база
                tmp_str = current_item.parent().parent().text(0) + '.' + tmp_str
        tmp_str += current_item.text(0)

        # Проверяем и добавляем или удаляем элемент из результирующего массива
        if tmp_str in self.arr_of_selected_item_in_tree:
            self.arr_of_selected_item_in_tree.remove(tmp_str)
        else:
            self.arr_of_selected_item_in_tree.append(tmp_str)

    def load_child_for_item(self, func_load_schemas=None, func_load_tables=None):
        current_item = self.tree_widget.currentItem()

        # Тип элемента (база, схема, таблица)
        type_of_item = check_type_of_item(current_item)


        if type_of_item == 'table': return

        if type_of_item == 'database':
            result_obj = func_load_schemas()
            self.add_children_to_parent_item(result_obj, current_item)
            print(current_item.children())


        print(type_of_item)
        # print(self.tree_widget.currentItem().text(0))
