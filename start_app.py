from PyQt5 import QtWidgets, QtCore

from Modules.Layouts.MainWindow import MainLayout

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    window = MainLayout()
    window.setWindowTitle('DUMP')

    # window.dialect_box.setFixedWidth(180)
    # window.settings_box.setMinimumWidth(500)

    # dialect_box.out_window - окно списка диалектов
    window.dialect_box.out_window.setFixedWidth(150)
    window.dialect_box.out_window.setMaximumHeight(len(window.dialect_box.list_dialects) * 30 + 5)
    window.main_layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
    # print(window.dialect_box.count_of_dialects)
    window.dialect_box.out_window.setStyleSheet("QGroupBox {background-color: #98a0a5}")

    # settings_box - окно настроек и дерева для диалекта
    window.settings_box.setMinimumWidth(800)
    window.settings_box.setAlignment(QtCore.Qt.AlignHCenter)
    window.settings_box.setFlat(True)

    window.show()

    sys.exit(app.exec_())
