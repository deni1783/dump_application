from PyQt5 import QtCore
from modules.my_classes.ClassForCMD.for_cmd import run_cmd
from modules.my_classes.custom_functions import write_to_log



class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str, str)

    def __init__(self, dialect, list_of_cmd, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.list_cmd = list_of_cmd
        self.dialect_name = dialect
        self.cmd = None
        self.code = None
        self.stdout = None
        self.stderr = None
        self.object = None

    def run(self):
        for i in self.list_cmd:
            self.sleep(2)
            self.object = i[0]
            self.cmd = i[1]
            print(self.cmd)
            (self.code, self.stdout, self.stderr) = run_cmd(self.cmd)
            write_to_log(self.dialect_name, self.object,
                         self.stdout, self.code,
                         self.stderr)
            self.mysignal.emit(self.object, str(self.code))
