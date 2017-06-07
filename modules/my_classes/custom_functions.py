from PyQt5 import QtWidgets, QtCore
import os
from datetime import datetime


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

def write_to_log(dialect: str, obj: str, log: str, status: str, stderr: str):
    """

    :param dialect: Название диалетка
    :param obj: Название объекта (база.схема.таблица)
    :param log: Вывод запущеной команды
    :param status: Статус завершения команды (0 - успех)
    :param stderr: Если была ошибка то текст ошибки
    :return: Записывает данные сразу в файл Logs/{datetime.now().date()}.log
    """
    # Открываем файл на дозапись в конец файла
    curr_date = str(datetime.now().date())
    log_file = open('Logs/' + curr_date + '.log', 'a')


    if status:
        stat = ('Fail!\n' + '\t\tError code: ' + str(status) + '\n'
                + '\t\tError text: ' + stderr)
    else:
        stat = 'Success!'
    separate = '=' * 80 + '\n'

    log_file.write(separate)
    log_file.write('Dialect: {}\n'.format(dialect))
    log_file.write('Object: ' + obj + '\n')
    log_file.write('Timestamp: ' + str(datetime.now()) + '\n')
    log_file.write('Status: ' + stat + '\n')
    log_file.write('-' * 40 + '\n\n')
    log_file.write(log)
    log_file.write(separate + '\n\n')

    log_file.close()

