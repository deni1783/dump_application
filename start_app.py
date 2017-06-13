from PyQt5 import QtWidgets

from modules.Layouts.MainWindow import MainLayout

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    window = MainLayout()
    window.setWindowTitle('DUMP')

    # window.dialect_box.setFixedWidth(180)
    # window.settings_box.setMinimumWidth(500)

    # dialect_box.out_window - окно списка диалектов
    window.dialect_box.out_window.setFixedWidth(150)
    window.dialect_box.out_window.setMaximumHeight(500)
    window.dialect_box.out_window.setStyleSheet("QGroupBox {background-color: #98a0a5}")

    # settings_box - окно настроек и дерева для диалекта
    window.settings_box.setMinimumWidth(800)

    window.show()

    sys.exit(app.exec_())
