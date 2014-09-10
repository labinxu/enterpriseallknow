from PyQt5 import QtWidgets


class TaskRunningTable(QtWidgets.QTableWidget):
    def __init__(self, parent):
        super(TaskRunningTable, self).__init__(parent)

    def contextMenuEvent(self, event):
        print(event.pos())
