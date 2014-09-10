import sys
if '../' not in sys.path:
    sys.path.append('../')
from PyQt5 import QtWidgets

from ui_templates.mainframe_ui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.lw_processing_tasks.insertRow(0)
        pc = QtWidgets.QProgressBar(self.ui.lw_processing_tasks)
        pc.setTextVisible(False)
        pc.setRange(0, 100)
        pc.setValue(10)
        self.ui.lw_processing_tasks.setCellWidget(0, 1, pc)

        self.ui.lw_processing_tasks.insertRow(1)
        pc = QtWidgets.QProgressBar(self.ui.lw_processing_tasks)
        pc.setTextVisible(False)
        pc.setRange(0, 100)
        pc.setValue(20)
        self.ui.lw_processing_tasks.setCellWidget(1, 1, pc)
        self.ui.lw_processing_tasks.insertRow(2)
        pc = QtWidgets.QProgressBar(self.ui.lw_processing_tasks)
        pc.setTextVisible(False)
        pc.setRange(0, 100)
        pc.setValue(30)
        self.ui.lw_processing_tasks.setCellWidget(2, 1, pc)
        pc.setTextVisible(False)


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
