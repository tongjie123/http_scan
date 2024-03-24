from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QAction, QFileDialog, QMessageBox
from PyQt5.uic import loadUi

from entity.http.HttpLogClass import HttpLog
from pyqt_api.TabWindowClass import TabWindow
from service.HttpServiceClass import HttpService
from windows.LogWindowClass import LogWindow

"""
主窗口
"""


class HomeWindow:
    def __init__(self):
        self.window = loadUi('ui/home.ui')
        self.window: QMainWindow
        # 最大化显示
        self.window.showMaximized()
        # 设置窗口标题
        self.window.setWindowTitle('http_scan v0.1')

        """
        子窗口
        """
        self.window.tabWidget: QTabWidget
        # 清除tab页
        self.window.tabWidget.clear()
        # tab窗口声明
        self.logTab_window = None
        # 加载tab页
        self.tabWidget_add_windows()

        """
        菜单栏
        """
        self.menuBar = self.window.menuBar()
        self.logMenu = self.menuBar.addMenu('日志')
        self.logMenu.addAction('初始化日志')
        self.logMenu.addAction('导入burp日志')
        self.databaseMenu = self.menuBar.addAction('数据库')
        self.menuBar.triggered.connect(self.menuBar_triggered)

        self.httpService = HttpService()

    def tabWidget_add_windows(self):
        # 日志窗口
        self.logTab_window = TabWindow(home_window=self, class_type=LogWindow)
        self.window.tabWidget.addTab(self.logTab_window.window, '日志')

    def menuBar_triggered(self, act: QAction):
        if act.text() == '初始化日志':
            self.httpService.truncate()
        elif act.text() == '导入burp日志':
            log_filePath, _ = QFileDialog.getOpenFileName(self.window, '选择日志文件', '')
            if log_filePath != '':
                httpLog = HttpLog()
                http_list = httpLog.read(log_filePath)
                for i in range(len(http_list)):
                    self.httpService.insert(http_list[i])
            QMessageBox.information(self.window, '提示', '导入完成')
        elif act.text() == '数据库':
            pass
