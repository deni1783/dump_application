from PyQt5 import QtWidgets, QtCore, QtGui
# from functools import partial


def clear_parent_tree_widget_item(parent):
    for i in reversed(range(parent.childCount())):
        parent.removeChild(parent.child(i))


def check_type_of_item(item):
    type_is = 'title_tree'
    try:
        item.parent().parent().parent().parent()
        type_is = 'table'
    except:
        try:
            item.parent().parent().parent()
            type_is = 'schema'
        except:
            try:
                item.parent().parent()
                type_is = 'database'
            except:
                    pass
    return type_is


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
        self.tree_widget.sortByColumn(0, QtCore.Qt.AscendingOrder)  # Сортировка
        self.tree_widget.setAnimated(True)

        self.top_level_database = QtWidgets.QTreeWidgetItem(self.tree_widget)
        self.top_level_database.setText(0, "Databases")


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




    def add_children_to_parent_item(self, child_arr, parent):
        parent_type = check_type_of_item(parent)

        # тип детей, он используется для иконок
        child_type = self.get_type_of_child(parent)

        # полность очищаем родитель перед добавление детей для таблиц
        if parent_type != 'table':
            clear_parent_tree_widget_item(parent)



        # Добавляем детей
        for item in child_arr:
            child = QtWidgets.QTreeWidgetItem(parent)
            child.setText(0, "{}".format(item))
            child.setIcon(0, QtGui.QIcon("icons/{}.png".format(child_type)))
            child.setFlags(child.flags() | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
            child.setCheckState(0, QtCore.Qt.Unchecked)



    # def clicked_item(self):
    #     current_item = self.tree_widget.currentItem()
    #
    #     # Статус флага (0 - не выбран, 1 - частично выбран, 2 - выбран)
    #     checked_status = current_item.checkState(0)
    #     if checked_status == 0:
    #         current_item.setCheckState(0, QtCore.Qt.Checked)
    #     else:
    #         current_item.setCheckState(0, QtCore.Qt.Unchecked)
    #
    #     # Вычисляем родителей
    #     tmp_str = ''
    #     if current_item.parent():
    #         # Если есть то либо схема, либо база
    #         tmp_str += current_item.parent().text(0) + '.'
    #         if current_item.parent().parent():
    #             # Если есть то это точно база база
    #             tmp_str = current_item.parent().parent().text(0) + '.' + tmp_str
    #     tmp_str += current_item.text(0)
    #
    #     # Проверяем и добавляем или удаляем элемент из результирующего массива
    #     if tmp_str in self.arr_of_selected_item_in_tree:
    #         self.arr_of_selected_item_in_tree.remove(tmp_str)
    #     else:
    #         self.arr_of_selected_item_in_tree.append(tmp_str)

    def load_child_for_item(self, func_load_databases=None, func_load_schemas=None, func_load_tables=None):

        # Изменяем курсор в песочные часы
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        current_connecting_settings = self.settings[self.combo_box_list_profiles.currentText()]

        # Тип элемента (база, схема, таблица)
        current_item = self.tree_widget.currentItem()
        child_type = self.get_type_of_child(current_item)


        if child_type == 'database':
            result_obj = func_load_databases(current_connecting_settings)
            self.add_children_to_parent_item(result_obj, current_item)


        if child_type == 'schema':
            current_connecting_settings["database"] = current_item.text(0)
            result_obj = func_load_schemas(current_connecting_settings, current_item.text(0))
            self.add_children_to_parent_item(result_obj, current_item)

        if child_type == 'table':
            current_connecting_settings["database"] = current_item.parent().text(0)
            result_obj = func_load_tables(current_connecting_settings, current_item.text(0))
            self.add_children_to_parent_item(result_obj, current_item)

        # Возвращаем обычный курсор
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)


    def get_checked_items_from_tree(self):
        checked_items = dict()

        root = self.top_level_database
        database_count = root.childCount()
        for i in range(database_count):
            database = root.child(i)
            database_text = database.text(0)

            # Если он чекнут (полность либо частично)
            if database.checkState(0) != 0:
                checked_items[database_text] = dict()

                for s in range(database.childCount()):
                    schema = root.child(i).child(s)
                    schema_text = schema.text(0)

                    if schema.checkState(0) != 0:
                        checked_items[database_text][schema_text] = list()

                        for t in range(schema.childCount()):
                            table = root.child(i).child(s).child(t)
                            table_text = table.text(0)

                            if table.checkState(0) != 0:
                                checked_items[database_text][schema_text].append(table_text)
        return checked_items

    @staticmethod
    def get_type_of_child(parent):
        parent_type = check_type_of_item(parent)
        if parent_type == 'database':
            return 'schema'
        elif parent_type == 'schema':
            return 'table'
        elif parent_type == 'title_tree':
            return 'database'

    def get_selected_type_of_dump(self):
        for r in (self.radio_only_data_type, self.radio_only_schema_type, self.radio_both_type):
            if r.isChecked():
                return r
