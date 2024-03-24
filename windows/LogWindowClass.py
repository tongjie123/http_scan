from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QTreeWidget, QFrame, QHBoxLayout, QMenu, QAction, QTableWidget, QTreeWidgetItem
from PyQt5.uic import loadUi

from entity.http.UrlClass import Url
from pyqt_api import QTreeWidgetModule
from windows.little_windows.LogFilterWindowClass import LogFilterWindow
from windows.little_windows.LogTableWindowClass import LogTableWindow

"""
日志窗口
"""


class LogWindow:
    def __init__(self, home_window):
        self.window = loadUi('ui/log.ui')
        self.home_window = home_window

        """
        树组件
        """
        self.window.treeWidget: QTreeWidget
        self.window.treeWidget.header().hide()
        self.window.treeWidget.setColumnCount(1)
        # 右键菜单
        self.window.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.window.treeWidget.customContextMenuRequested.connect(self.treeWidget_rightMenu)
        # 点击
        self.window.treeWidget.itemClicked.connect(self.treeWidget_itemClicked)

        """
        日志表格组件
        """
        self.logTable_window = LogTableWindow(self)
        self.window.frame: QFrame
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.logTable_window.window)
        self.window.frame.setLayout(self.layout)

        # 过滤窗口
        self.logFilter_window = LogFilterWindow(parent_window=self)
        # 过滤按钮
        self.window.pushButton: QPushButton
        self.window.pushButton.clicked.connect(self.logFilter_window.window.show)
        # 表格设置按钮
        self.window.pushButton_2: QPushButton
        self.action_dict = {}
        self.init_menu()

    """
    测试、直接请求、爆破导致的新增日志，传递过来其id，与当前日志窗口的sql语句拼接，判断是否符合条件，从而输出
    """

    def append_http(self, http_id):
        pass

    def load(self):
        # 根据显示条件执行
        self.logFilter_window.show_filter()

    def init_menu(self):
        value_list = self.logTable_window.header_list.copy()
        menu = QMenu()
        for i in range(len(value_list)):
            action = QAction(value_list[i])
            action.setCheckable(True)
            action.isChecked()
            action.setChecked(True)
            menu.addAction(action)
            self.action_dict.update({value_list[i]: action})
        self.window.pushButton_2: QPushButton
        self.window.pushButton_2.setMenu(menu)
        self.window.pushButton_2.menu().triggered.connect(self.menu_triggered)
        # 设置初始时未选中的action
        # self.action_dict.get('id').setChecked(False)

    def menu_triggered(self):
        key_list = self.action_dict.keys()
        key_isChecked_list = list()
        for key in key_list:
            if self.action_dict.get(key).isChecked():
                key_isChecked_list.append(key)
        self.logTable_window.tableWidget_setColumns(key_isChecked_list)

    def treeWidget_addItem(self, u: Url):
        arr = u.address_arr()
        QTreeWidgetModule.treeWidget_addPathArr(treeWidget=self.window.treeWidget, pathArr=arr)

    def treeWidget_rightMenu(self, pos):
        pass

    def treeWidget_itemClicked(self, item: QTreeWidgetItem, column: int):
        url_pre = QTreeWidgetModule.treeWidget_getPath(item)
        print(url_pre)
        # 拒绝http://www.baidu.com/abc匹配到http://www.baidu.com/abcdefg
        self.logFilter_window.show_filter_with('url regexp "'+url_pre+'(/|$|\\\\?)"')