import sys
if '../' not in sys.path:
    sys.path.append('../')
import os
import math
import threading
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QAction, QFileDialog)
from PyQt5.QtGui import (QIcon, QKeySequence)
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from db.excel import PyExcel
from utils import debug
from typesdefine import (Task, MakeTaskObj, Enterprise)
from manager.taskmanager import TaskManager
from ui_templates.mainframe_ui import Ui_MainWindow
from ui_templates.site_select_dlg import Ui_Dialog
from multiprocessing import freeze_support
from functools import partial
from appconfig import appconfig
# for cx_freeze fixed
sys.stdout = open('run.log', 'a')
sys.stderr = sys.stdout
freeze_support()


def PromptMessage(self, msg):
        QtWidgets.QMessageBox.about(self, "about", msg)


class SiteSelect(QtWidgets.QDialog):
    def __init__(self, parent=None, language_index=1):
        super(SiteSelect, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.lanugageIndex = language_index
        self.sites = appconfig.getSites()
        self.initSites()

    def onCellClicked(self, row, col):
        self.currentSelectedItem = self.ui.tw_sites.item(row, col)
        self.accept()

    def currentSelectItem(self):
        return self.currentSelectedItem

    def initSites(self):
        row = 0
        col = 0
        size = len(self.sites)
        countRow = math.ceil(size/3)
        self.ui.tw_sites.setRowCount(countRow)
        self.ui.tw_sites.setColumnCount(3)
        for index, site in enumerate(self.sites):
            if index != 0 and index % 3 == 0:
                row += 1
                col = 0
            item = QtWidgets.QTableWidgetItem()
            item.setText(site[self.lanugageIndex])
            self.ui.tw_sites.setItem(row, col, item)
            col += 1


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

        # conf
        # ###################################
        self.changeStyle('Windows')
        self.language = appconfig.getLanguage()
        self.lanugageIndex = self.language == 'english' and 0 or 1
        self.sites = appconfig.getSites()
        # tab initNewTaskTab
        self.initNewTaskTab()
        # ############################################
        self.createActions()
        self.createToolbar()
        self.initTableTitles()
        self.initSignals()
        self.signalCreatedSuccessful.connect(self.onCreatedSuccessful)
        # ###################################
        self.signalCreatedSuccessful.emit()
        # for dbug
        # self.appendTask('task1')
        # self.appendTask('task2')
        # self.appendTask('task3')
        # self.appendFinished('finishedTask1')
        # self.appendFinished('finishedTask2')
        # self.appendFinished('finishedTask3')

    def initNewTaskTab(self):
        self.ui.lb_current_site.setText(self.sites[0][self.lanugageIndex])

    @pyqtSlot()
    def on_actionDebug_triggered(self):
        if debug.getLevel() == 10:
            debug.setLevel(20)
            self.ui.statusbar.clearMessage()
        else:
            debug.setLevel(10)
            self.ui.statusbar.showMessage("debug mode")

    def changeStyle(self, styleName):
        style = QtWidgets.QStyleFactory.create(styleName)
        QtWidgets.QApplication.setStyle(style)

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
        self.__fillTableTitle(finishedTasks,
                              self.tabTitles,
                              self.lanugageIndex)
        
        processingTasks = self.ui.tw_processing_task_details
        self.__fillTableTitle(processingTasks,
                              self.tabTitles,
                              self.lanugageIndex)

        # init tab map
        for i, value in enumerate(self.tabTitles):
            self.tabmap[value[0]] = i

    def appendFinished(self, taskname):
        self.ui.lw_finished_tasks.addItem(taskname)

    def onTaskCompleted(self, taskname):
        debug.info('task %s finished' % taskname)
        count = self.ui.lw_processing_tasks.rowCount()
        for i in range(count):
            item = self.ui.lw_processing_tasks.item(i, 0)
            if item.text() == taskname:
                self.ui.lw_processing_tasks.removeRow(i)
                self.appendFinished(taskname)
                break

    def onCreatedSuccessful(self):
        self.initTaskManager()
        threading.Thread(target=self.guiMonitor, args=()).start()
        threading.Thread(target=self.updateTaskProgress, args=()).start()

        self.onTabBarClicked(self.ui.tabWidget.currentIndex())

    def closeEvent(self, event):
        debug.info('received close event')
        self.taskManager.addTask(None)
        self.stop = True
        return event.accept()
    # ##################################################################
    # widget operator

    def onFinishedTasksItemClicked(self, item):
        taskname = item.text()
        self.taskManager.resetDb('%s.db' % taskname)
        if taskname not in self.taskResult.keys():
            objects = Enterprise.objects().all()
            self.taskResult[taskname] = objects
        else:
            objects = self.taskResult[taskname]
        self._fillCompaniesTable(self.ui.tw_finished_task_details, objects)

    def onProcessTasksRClicked(self, item):
        self.actionRestart = QAction('Restart', self,
                                     triggered=partial(self.restartTask, item))

        self.actionStopTask = QAction('Stop', self,
                                      triggered=partial(self.stopTask, item))

        self.actionStopTaskAll = QAction('StopAll', self,
                                         triggered=self.stopTaskAll)

        popMenu = QtWidgets.QMenu()
        popMenu.addAction(self.actionRestart)
        popMenu.addAction(self.actionStopTask)
        popMenu.addAction(self.actionStopTaskAll)
        popMenu.exec(self.cursor().pos())

    def onFinishedTasksRClicked(self, item):
        popMenu = QtWidgets.QMenu()
        trigger = partial(self.exportToExcel, item)
        self.actionExportToExcel = QAction('ExportToExcel', self,
                                           triggered=trigger)

        trigger = partial(self.deleteTask, item)
        self.actionDeleteTask = QAction('Delete', self,
                                        triggered=trigger)

        trigger = partial(self.deleteTaskFromDisk, item)
        self.actionDeleteTaskFromDisk = QAction('DeleteFromDisk', self,
                                                triggered=trigger)

        popMenu.addAction(self.actionExportToExcel)
        popMenu.addSeparator()

        popMenu.addAction(self.actionDeleteTask)
        popMenu.addAction(self.actionDeleteTaskFromDisk)
        popMenu.exec(self.cursor().pos())

    def onTabBarClicked(self, index):
        # self._promptMessage(self.ui.tabWidget.tabText(index))

        if index == 1:
            self.taskManager.resetDb('tasks.db')
            # self.ui.lw_processing_tasks.clear()
            self.ui.lw_processing_tasks.setRowCount(0)
            tasks = Task.objects().filter('task_status="0"')
            for task in tasks:
                self.appendTask(task)

        elif index == 2:
            self.taskManager.resetDb('tasks.db')
            self.ui.lw_finished_tasks.clear()
            tasks = Task.objects().filter('task_status="1"')
            for task in tasks:
                self.ui.lw_finished_tasks.addItem(task.task_name)

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

    # ##########################################################################

    def appendTask(self, task):
        taskName = task.task_name
        index = self.ui.lw_processing_tasks.rowCount()
        self.ui.lw_processing_tasks.insertRow(index)
        pc = QtWidgets.QProgressBar(self.ui.lw_processing_tasks)
        pc.setTextVisible(False)
        pc.setRange(0, 100)
        pc.setValue(1)
        item = QtWidgets.QTableWidgetItem()
        item.setText(taskName)
        self.ui.lw_processing_tasks.setItem(index, 0, item)
        self.ui.lw_processing_tasks.setCellWidget(index, 1, pc)

    def hasSameTask(self, taskName):
        self.taskManager.resetDb('tasks.db')
        tasks = Task.objects().filter('task_name="%s"' % taskName)
        if tasks:
            return True
        return False

    def onSelectSite(self):
        siteSelect = SiteSelect(self)
        siteSelect.exec_()
        item = siteSelect.currentSelectItem()
        if item:
            self.ui.lb_current_site.setText(item.text())
        else:
            self.onSelectSite()

    def getSearchModule(self, siteName):
        for site in self.sites:
            if siteName == site[self.lanugageIndex]:
                self._promptMessage(site[0])
                return site[0]
        
    def onNewTask(self):

        taskName = self.ui.le_task_name.text()
        siteName = self.ui.lb_current_site.text()
        siteName = self.getSearchModule(siteName)

        keyWords = self.ui.le_search_keywords.text()
        if not (taskName and siteName and keyWords):
            return
        if self.hasSameTask(taskName):
            QtWidgets.QMessageBox.warning(self,
                                          'Error',
                                          'Already have same task')
            return

        newTask = Task(task_name=taskName,
                       task_site_name=siteName,
                       task_search_words=keyWords,
                       task_status=0,
                       task_progress=0)

        self.appendTask(newTask)
        self.startTask(newTask)

        self.ui.le_task_name.setText("")
        self.ui.le_search_keywords.setText("")
        self.ui.tabWidget.setCurrentIndex(1)

    def startTask(self, task):
        self.taskManager.resetDb('tasks.db')
        task.save()
        self.taskManager.addTask(task)
        debug.error('new Task id %s' % task.id)

    def createActions(self):
        self.newTaskAct = QAction(QIcon('../resource/images/new.png'),
                                  "&New Task",
                                  self, shortcut=QKeySequence.New,
                                  statusTip="Create a new task")
        # triggered=self.newTask)

    def _promptMessage(self, msg):
        QtWidgets.QMessageBox.about(self, "about", msg)

    def stopTask(self, item):
        self._promptMessage(item.text())

    def stopTaskAll(self):
        pass

    def restartTask(self, item):
        objs = Task.objects().filter('task_name="%s"' % item.text())
        if objs:
            task = MakeTaskObj(objs[0])
            self.startTask(task)
        
    def deleteTask(self, item):
        self.taskManager.resetDb('tasks.db')
        taskName = item.text()
        tasks = Task.objects().filter('task_name="%s"' % taskName)
        task = MakeTaskObj(tasks[0])
        task.task_status = '2'
        task.save()
        self.onTabBarClicked(2)

    def deleteTaskFromDisk(self, item):
        taskName = item.text()
        self._promptMessage('delete from disk %s' % taskName)

    def exportToExcel(self, item):
        taskname = item.text()

        self.taskManager.resetDb('%s.db' % taskname)
        if taskname not in self.taskResult.keys():
            objects = Enterprise.objects().all()
            self.taskResult[taskname] = objects
        else:
            objects = self.taskResult[taskname]
        titles = sorted(self.tabmap.items(),
                        key=lambda item: item[1])

        options = QFileDialog.Options()

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

    # #####################################################################
    # #### threading
    def updateTaskProgress(self):
        debug.info('start update task progress')
        while True and not self.stop:
            tasks_status = self.taskManager.running_tasks_status
            try:
                for taskName, progress in tasks_status.items():
                    tasks = self.ui.lw_processing_tasks
                    count = tasks.rowCount()
                    for index in range(count):
                        item = tasks.item(index, 0)
                        name = item.text()
                        if name == taskName:
                            self.signalUpdateTaskProgress.emit(index,
                                                               1,
                                                               progress)
            finally:
                pass
            time.sleep(1)

    def guiMonitor(self):
        debug.info("start gui monitor")
        task = self.taskManager.popFinisedTask()
        while task is not None:
            self.taskManager.resetDb('tasks.db')
            self.signalTaskCompleted.emit(task.task_name)
            task.task_status = '1'
            task.task_progress = '100'
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
