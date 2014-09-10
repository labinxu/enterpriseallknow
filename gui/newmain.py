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
#        btn = QtWidgets.QPushButton(self.ui.lw_processing_tasks)
#        btn.setText('12/1/12')
#        self.ui.lw_processing_tasks.setCellWidget(0, 0, btn)
        
#        self.ui.lw_processing_tasks.setCellWidget(1, 0, btn)
        pc = QtWidgets.QProgressBar(self.ui.lw_processing_tasks)
        pc.setRange(0, 100)
        pc.setValue(10)
        self.ui.lw_processing_tasks.setCellWidget(0, 0, pc)
        pc = QtWidgets.QProgressBar(self.ui.lw_processing_tasks)
        pc.setRange(0, 100)
        pc.setValue(20)
        self.ui.lw_processing_tasks.setCellWidget(1, 0, pc)
        
        pc = QtWidgets.QProgressBar(self.ui.lw_processing_tasks)
        pc.setRange(0, 100)
        pc.setValue(30)
        self.ui.lw_processing_tasks.setCellWidget(2, 0, pc)
        
        pc = QtWidgets.QProgressBar(self.ui.lw_processing_tasks)
        pc.setRange(0, 100)
        pc.setValue(40)
        self.ui.lw_processing_tasks.setCellWidget(3, 0, pc)
        
        self.ui.lw_processing_tasks.insertRow(4)
        pc = QtWidgets.QProgressBar(self.ui.lw_processing_tasks)
        pc.setRange(0, 100)
        pc.setValue(50)
        
        self.ui.lw_processing_tasks.insertRow(5)
        self.ui.lw_processing_tasks.setCellWidget(4, 0, pc)
        pc = QtWidgets.QProgressBar(self.ui.lw_processing_tasks)
        pc.setRange(0, 100)
        pc.setValue(60)
        self.ui.lw_processing_tasks.setCellWidget(5, 0, pc)

        print(self.ui.lw_processing_tasks.verticalHeaderItem(3).text())

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
