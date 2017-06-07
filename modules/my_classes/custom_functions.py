from PyQt5 import QtWidgets, QtCore
import os

def set_cursor_style(style: str):

    if style == 'wait':
        # Изменяем курсор в песочные часы
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
    elif style == 'normal':
        # Возвращаем обычный курсор
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)


# Параметры: 1 - Начальная директорыя, 2 - название файла
# Функция возвращает нормализированный путь к файлу или None если файл отсутствует
def get_path_to_file(start_dir, file_name):
    root = os.walk(start_dir)
    for path, dir, files in root:
        for f in files:
            if f == file_name:
                out_path = os.path.join(path, f)
                return os.path.normcase(out_path)

def wrap_double_quotes(s: str):
    return '"' + s + '"'
