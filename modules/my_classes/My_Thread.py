from PyQt5 import QtCore
from modules.my_classes.ClassForCMD.for_cmd import run_cmd

from modules.my_classes.custom_functions import write_to_log

class MyThread(QtCore.QThread):
    """
    Клас для создания потоков в котором:

    Запускается cmd (ДАМП)
    А так же записывает данные в лог файл

    list_of_cmd = ["object for dump (DB.SCHEMA.TABLE)", "строка для запуска в CMD"]
    """
    mysignal = QtCore.pyqtSignal(str, str)

    def __init__(self, dialect_name, list_of_cmd, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.list_cmd = list_of_cmd
        self.dialect = dialect_name
        self.cmd = None
        self.code = None
        self.stdout = None
        self.stderr = None
        self.object = None

    def run(self):
        for i in self.list_cmd:
            self.sleep(1)  # Временный таймер
            self.object = i[0]
            self.cmd = i[1]
            # Запуск CMD команды
            (self.code, self.stdout, self.stderr) = run_cmd(self.cmd)

            # Запись в файл лога
            write_to_log(self.dialect, self.object, self.stdout, self.code, self.stderr)

            # Сигнал
            self.mysignal.emit(self.object, str(self.code))
