# !/usr/bin/env python
# coding=utf-8
import sys
import os
import time
import threading
if '../' not in sys.path:
    sys.path.append('../')
import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
from ui_templates.ui_mainframe import Ui_main_frame
# from ui_templates.ui_mainform import Ui_MainWindow

from manager.taskmanager import TaskManager
from typesdefine import Task, Enterprise
from utils import debug
from multiprocessing import freeze_support
# for cx_freeze fixed
sys.stdout = open('run.log', 'a')
sys.stderr = sys.stdout
freeze_support()


class MainFrame(QDialog):
    signalTaskCompleted = pyqtSignal(str)
    signalCreatedSuccessful = pyqtSignal()
    signalUiOutputUpdate = pyqtSignal(str)
    signalUpdateTaskProgress = pyqtSignal(str, float)

    def __init__(self, parent=None):
        super(MainFrame, self).__init__(parent)
        self.ui = Ui_main_frame()
        self.ui.setupUi(self)
        self.initResultView()
        self.taskManager = None
        self.taskResult = {}
        self.stop = False
        # actions
        self.actionExportToExcel = QtWidgets.QAction('Export to excel',
                                                     self.ui.lw_finished_tasks)
        # signals
        self.signalTaskCompleted.connect(self.onTaskCompleted)
        self.signalUiOutputUpdate.connect(self.output)
        self.signalUpdateTaskProgress.connect(self.updateTaskProgress)
        debug.setOutputSignal(self.signalUiOutputUpdate)

        # end __init__
        self.signalCreatedSuccessful.connect(self.onCreatedSuccessful)
        self.signalCreatedSuccessful.emit()

    def on_actionExportToExcel_triggered(self):
        debug.info('actionExportToExcel')

    def output(self, msg):
        self.ui.lw_output.addItem(msg)

    def updateTaskProgress(self):
        debug.info('start update task progress')
        while True and not self.stop:
            tasks_status = self.taskManager.running_tasks_status
            for taskName, progress in tasks_status.items():
                tasks = self.ui.lw_processing_tasks
                count = tasks.count()
                for index in range(count):
                    item = tasks.item(index)
                    name = item.text()
                    if name == taskName:
                        debug.info('%s %s' % (taskName, progress) + '%')
            time.sleep(1)

    def onCreatedSuccessful(self):
        self.initTaskManager()
        threading.Thread(target=self.guiMonitor, args=()).start()
        threading.Thread(target=self.updateTaskProgress, args=()).start()

    def initTaskManager(self):
        # task relations
        self.taskManager = TaskManager()
        self.taskManager.setDb('tasks.db')
        self.taskManager.start()

    def initResultView(self):
        self.tabmap = {}
        self.tabmap["company_name"] = 0
        self.tabmap["company_contacts"] = 1
        self.tabmap["company_phone_number"] = 2
        self.tabmap["company_mobile_phone"] = 3
        self.tabmap["company_fax"] = 4
        self.tabmap["company_postcode"] = 5
        self.tabmap["company_website"] = 6
        self.tabmap["company_addr"] = 7
        self.tabmap["company_details"] = 8
        self.tabmap['id'] = 9

    def guiMonitor(self):
        debug.info('start gui monitor')
        while True:
            try:
                task = self.taskManager.popFinisedTask()
                if task is None:
                    break
                self.taskManager.resetDb('tasks.db')
                self.signalTaskCompleted.emit(task.task_name)
                task.save()
            except:
                pass
            time.sleep(3)

    def _fillCompaniesTable(self, tableWidget, objects):

        tableWidget.setRowCount(len(objects))
        row = 0
        for ent in objects:
            for name, var in vars(ent).items():
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(var))
                tableWidget.setItem(row, self.tabmap[name], item)
            row += 1

    def onLWProcessingTasksItemClicked(self, item):
        taskname = item.text()
        self.taskManager.resetDb('%s.db' % taskname)
        if taskname not in self.taskResult.keys():
            objects = Enterprise.objects().all()
        else:
            objects = self.taskResult[taskname]
        self._fillCompaniesTable(self.ui.tw_processing_task_details, objects)

    def onLWFinishedTasksItemClicked(self, item):
        taskname = item.text()
        self.taskManager.resetDb('%s.db' % taskname)
        if taskname not in self.taskResult.keys():
            objects = Enterprise.objects().all()
        else:
            objects = self.taskResult[taskname]
        self._fillCompaniesTable(self.ui.tw_finished_task_details, objects)
        return
        self.ui.tw_finished_task_details.setRowCount(len(objects))
        row = 0
        for ent in objects:
            for name, var in vars(ent).items():
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(var))
                self.ui.tw_finished_task_details.setItem(row,
                                                         self.tabmap[name],
                                                         item)
            row += 1

    def onTabBarClicked(self, index):
        if index == 2:
            self.taskManager.resetDb('tasks.db')
            self.ui.lw_finished_tasks.clear()
            tasks = Task.objects().filter('task_status="1"')
            for task in tasks:
                self.ui.lw_finished_tasks.addItem(task.task_name)
            self.ui.lw_finished_tasks.setCurrentItem(None)

    def onTaskCompleted(self, taskname):
        debug.info('task %s finished' % taskname)
        model = self.ui.lw_processing_tasks.model()
        for i in range(self.ui.lw_processing_tasks.count()):
            item = self.ui.lw_processing_tasks.item(i)
            if item.text() == taskname:
                model.removeRow(i)
                self.ui.lw_finished_tasks.addItem(taskname)
                break

    def hasSameTask(self, taskName):

        if os.path.exists('%s.db' % taskName):
            return False
        return True

    def onNewTaskClicked(self):
        '''Create a new task'''

        taskName = self.ui.le_task_name.text()
        siteName = self.ui.lb_current_site.text()
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
        self.ui.lw_processing_tasks.addItem(taskName)
        self.taskManager.addTask(newTask)
        msginfo = 'Task %s is running' % taskName
        debug.info(msginfo)

    def closeEvent(self, event):
        debug.info('received close evnet')
        self.taskManager.addTask(None)
        self.stop = True
        event.accept()

    def createMenuForFinishedTasks(self):
        popMenu = QtWidgets.QMenu()
        popMenu.addAction(self.actionExportToExcel)
        action = popMenu.exec(self.cursor().pos())
        return action

    def contextMenuEvent(self, event):
        # debug.info('right event x %s ,y %s' % (event.x(), event.y()))
        #
        curItem = None
        indexTab = self.ui.tbwg_menubar.currentIndex()
        # finished tasks
        if 2 == indexTab:
            curItem = self.ui.lw_finished_tasks.currentItem()
            if not curItem:
                return
            action = self.createMenuForFinishedTasks(self)
            if action == self.actionExportToExcel:
                self.onExportToExcel(curItem.text())
        if 1 == indexTab:
            pass

    # actions
    def onExportToExcel(self, taskName):
        debug.info('%s on export to excel' % taskName)


def main():
    import sys
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    window = MainFrame()
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
