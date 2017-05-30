from PyQt5 import QtWidgets
from modules.Layouts.MainWindow import MainLayout


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    window = MainLayout()
    window.setWindowTitle('DUMP')

    # window.dialect_box.setFixedWidth(180)
    # window.settings_box.setMinimumWidth(500)

    window.show()

    sys.exit(app.exec_())

"""
root = self.treeWidget.invisibleRootItem()
child_count = root.childCount()
for i in range(child_count):
    item = root.child(i)
    url = item.text(0) # text at first (0) column
    item.setText(1, 'result from %s' % url) # update result column (1)



checked = dict()
        root = self.tree_widget.invisibleRootItem()
        signal_count = root.childCount()

        for i in range(signal_count):
            signal = root.child(i)
            checked_sweeps = list()
            num_children = signal.childCount()

            for n in range(num_children):
                child = signal.child(n)

                if child.checkState(0) == QtCore.Qt.Checked:
                    checked_sweeps.append(child.text(0))

            checked[signal.text(0)] = checked_sweeps
"""