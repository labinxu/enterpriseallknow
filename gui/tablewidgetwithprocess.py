from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal


class Items:
    def __init__(self, data):
        self.items = data


class TaskRunningTable(QtWidgets.QTableWidget):
    cellContextClicked = pyqtSignal(QtWidgets.QTableWidgetItem)

    def __init__(self, parent):
        super(TaskRunningTable, self).__init__(parent)

    def contextMenuEvent(self, event):

        item = self.itemAt(event.pos())
        if item:
            self.cellContextClicked.emit(item)
