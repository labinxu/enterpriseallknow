from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal


class ListWidget(QtWidgets.QListWidget):
    cellContextClicked = pyqtSignal(QtWidgets.QListWidgetItem)

    def __init__(self, parent):
        super(ListWidget, self).__init__(parent)

    def contextMenuEvent(self, event):
        item = self.itemAt(event.pos())
        if item:
            self.cellContextClicked.emit(item)
