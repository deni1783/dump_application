from PyQt5 import QtWidgets
from modules.Layouts.MainWindow import MainLayout


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    window = MainLayout()
    window.setWindowTitle('DUMP')

    window.dialect_box.setFixedWidth(180)
    window.settings_box.setFixedWidth(500)

    window.show()

    sys.exit(app.exec_())
