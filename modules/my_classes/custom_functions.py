from PyQt5 import QtWidgets, QtCore


def set_cursor_style(style: str):

    if style == 'wait':
        # Изменяем курсор в песочные часы
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
    elif style == 'normal':
        # Возвращаем обычный курсор
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)