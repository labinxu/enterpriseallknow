import sys
if '../' not in sys.path:
    sys.path.append('../')
import os
import threading
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QAction, QFileDialog, QMessageBox)
from PyQt5.QtGui import (QIcon, QKeySequence)
from PyQt5.QtCore import pyqtSignal
from db.excel import PyExcel
from utils import debug
from typesdefine import (Task, Enterprise)
from manager.taskmanager import TaskManager
from ui_templates.mainframe_ui import Ui_MainWindow
from multiprocessing import freeze_support
# for cx_freeze fixed
sys.stdout = open('run.log', 'a')
sys.stderr = sys.stdout
freeze_support()


class MainWindow(QtWidgets.QMainWindow):
    signalTaskCompleted = pyqtSignal(str)
    signalCreatedSuccessful = pyqtSignal()
    signalUpdateTaskProgress = pyqtSignal(int, int, int)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.taskResult = {}
        self.tabTitles = []
        self.stop = False
        self.tabmap = {}

        self.createActions()
        self.createToolbar()
        self.initTableTitles()
        self.initSignals()

        self.signalCreatedSuccessful.connect(self.onCreatedSuccessful)
        self.signalCreatedSuccessful.emit()
    
    def initTaskManager(self):
        # task relations
        self.taskManager = TaskManager()
        self.taskManager.setDb('tasks.db')
        self.taskManager.start()

    def initSignals(self):
        self.signalTaskCompleted.connect(self.onTaskCompleted)
        self.signalUpdateTaskProgress.connect(self.onUpdateProgress)

    def __fillTableTitle(self, tablewidget, data, index):
        count = len(data)
        tablewidget.setColumnCount(count)
        for i, value in enumerate(data):
            item = QtWidgets.QTableWidgetItem()
            item.setText(value[index])
            tablewidget.setHorizontalHeaderItem(i, item)

    def initTableTitles(self):

        with open('./configure/tasktable.ini', encoding='utf8') as f:
            for line in f.readlines():
                items = line.split('=')
                eng = items[0]
                ch = items[1][:-1]
                self.tabTitles.append((eng, ch))

        # fill the tableWidget
        finishedTasks = self.ui.tw_finished_task_details
        self.__fillTableTitle(finishedTasks, self.tabTitles, 0)
        processingTasks = self.ui.tw_processing_task_details
        self.__fillTableTitle(processingTasks, self.tabTitles, 0)

        # init tab map
        for i, value in enumerate(self.tabTitles):
            self.tabmap[value[0]] = i

    def onTaskCompleted(self, taskname):
        debug.info('task %s finished' % taskname)
        count = self.ui.lw_processing_tasks.rowCount()
        for i in range(count):
            item = self.ui.lw_processing_tasks.item(i, 0)
            if item.text() == taskname:
                self.ui.lw_processing_tasks.removeRow(i)
                self.ui.lw_finished_tasks.addItem(taskname)
                break

        # model = self.ui.lw_processing_tasks.model()
        # for i in range(self.ui.lw_processing_tasks.count()):
        #     item = self.ui.lw_processing_tasks.item(i)
        #     if item.text() == taskname:
        #         model.removeRow(i)
        #         self.ui.lw_finished_tasks.addItem(taskname)
        #         break

    def onCreatedSuccessful(self):
        self.initTaskManager()
        threading.Thread(target=self.guiMonitor, args=()).start()
        threading.Thread(target=self.updateTaskProgress, args=()).start()

    def closeEvent(self, event):
        debug.info('received close evnet')
        self.taskManager.addTask(None)
        self.stop = True
        event.accept()

    # #######################################################################
    def _fillCompaniesTable(self, tableWidget, objects):

        tableWidget.setRowCount(len(objects))
        row = 0
        for ent in objects:
            for name, var in vars(ent).items():
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(var))
                tableWidget.setItem(row, self.tabmap[name], item)
            row += 1

    def onLWFinishedTasksItemClicked(self, item):
        taskname = item.text()
        self.taskManager.resetDb('%s.db' % taskname)
        if taskname not in self.taskResult.keys():
            objects = Enterprise.objects().all()
            self.taskResult[taskname] = objects
        else:
            objects = self.taskResult[taskname]
        self._fillCompaniesTable(self.ui.tw_finished_task_details, objects)

    # ##########################################################################

    def appendTask(self, taskName):
        index = self.ui.lw_processing_tasks.rowCount()
        self.ui.lw_processing_tasks.insertRow(index)
        pc = QtWidgets.QProgressBar(self.ui.lw_processing_tasks)
        pc.setTextVisible(False)
        pc.setRange(0, 100)
        pc.setValue(0)
        item = QtWidgets.QTableWidgetItem()
        item.setText(taskName)
        self.ui.lw_processing_tasks.setItem(index, 0, item)
        self.ui.lw_processing_tasks.setCellWidget(index, 1, pc)

    def hasSameTask(self, taskName):
        if os.path.exists('%s.db' % taskName):
            return False
        return True

    def onNewTask(self):
        self.ui.le_task_name.setText('r1')
        taskName = self.ui.le_task_name.text()
        siteName = self.ui.lb_current_site.text()
        self.ui.le_search_keywords.setText('keyboard')
        keyWords = self.ui.le_search_keywords.text()
        if not (taskName and siteName and keyWords):
            return
        if not self.hasSameTask(taskName):
            debug.info('Change task name please')
            return
        newTask = Task(task_name=taskName,
                       task_site_name=siteName,
                       task_search_words=keyWords,
                       task_status=0)

        self.appendTask(taskName)
        self.taskManager.addTask(newTask)

        msginfo = 'Task %s is running' % taskName
        debug.info(msginfo)
        self.ui.le_task_name.setText("")
        self.ui.le_search_keywords.setText("")

    def createActions(self):
        self.newTaskAct = QAction(QIcon('../resource/images/new.png'),
                                  "&New Task",
                                  self, shortcut=QKeySequence.New,
                                  statusTip="Create a new task")
        # triggered=self.newTask)

    def exportToExcel(self, taskname):
        # self.titles, self.tabmap = tabmap
        self.taskManager.resetDb('%s.db' % taskname)
        if taskname not in self.taskResult.keys():
            objects = Enterprise.objects().all()
        else:
            objects = self.taskResult[taskname]
        titles = sorted(self.tabmap.items(),
                        key=lambda item: item[1])

        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "QFileDialog",
                                                  '%s.xls' % taskname,
                                                  "All Files (*);;Excel(.xls)",
                                                  options=options)

        if os.path.exists(fileName):
            return
        pyExcel = PyExcel(fileName,
                          self.tabmap,
                          [i for i, j in titles],
                          objects)
        pyExcel.save()

    def createToolbar(self):
        self.ui.toolBar.addAction(self.newTaskAct)

    def onUpdateProgress(self, row, col, process):
        pc = self.ui.lw_processing_tasks.cellWidget(row, col)
        pc.setValue(process)
        debug.info('update process %d' % process)

    # #####################################################################
    # #### threading
    def updateTaskProgress(self):
        debug.info('start update task progress')
        while True and not self.stop:
            tasks_status = self.taskManager.running_tasks_status
            for taskName, progress in tasks_status.items():
                tasks = self.ui.lw_processing_tasks
                count = tasks.rowCount()
                for index in range(count):
                    item = tasks.item(index, 0)
                    name = item.text()
                    if name == taskName:
                        self.signalUpdateTaskProgress.emit(index, 1, progress)
            time.sleep(1)

    def guiMonitor(self):
        debug.info("start gui monitor")
        task = self.taskManager.popFinisedTask()
        while task is not None:
            self.taskManager.resetDb('tasks.db')
            self.signalTaskCompleted.emit(task.task_name)
            task.save()
            del self.taskManager.running_tasks_status[task.task_name]
            task = self.taskManager.popFinisedTask()


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
