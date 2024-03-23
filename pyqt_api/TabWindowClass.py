from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QTabWidget, QMenu, QAction
from PyQt5.uic import loadUi

"""
tab组件窗口，泛型，容纳其它具体的业务窗口
"""


class TabWindow:
    def __init__(self, home_window, class_type):
        self.window = loadUi('ui/tab.ui')
        # 主窗口
        self.home_window = home_window
        # 子窗口类型
        self.class_type = class_type

        """
        tab组件
        """
        self.window.tabWidget: QTabWidget
        # 右键菜单
        self.window.tabWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.window.tabWidget.customContextMenuRequested.connect(self.tabWidget_rightMenu)
        # 清除tab页
        self.window.tabWidget.clear()
        # 记录各tab页的窗口对象
        self.window_list = list()
        # tab页标识，新增tab页的text标识为该属性+1的str类型
        self.tab_order = 0

        # 初始添加
        self.add_sub_window()

    def add_sub_window(self):
        window = self.class_type(home_window=self.home_window)
        self.window.tabWidget: QTabWidget
        self.window_list.append(window)
        self.tab_order = self.tab_order + 1
        self.window.tabWidget.addTab(window.window, str(self.tab_order))

    def tabWidget_rightMenu(self, pos):
        menu = QMenu(self.window.tabWidget)
        menu.addAction('删除当前项')
        menu.addAction('清除')
        menu.addAction('新增')
        menu.triggered.connect(self.tabWidget_rightMenu_triggered)
        menu.exec_(QCursor.pos())

    def tabWidget_rightMenu_triggered(self, act: QAction):
        self.window.tabWidget: QTabWidget
        if act.text() == '清除':
            self.window.tabWidget.clear()
        elif act.text() == '新增':
            self.add_sub_window()
        elif act.text() == '删除当前项':
            i = self.window.tabWidget.currentIndex()
            if i >= 0:
                self.window.tabWidget.removeTab(i)
                self.window_list.pop(i)
