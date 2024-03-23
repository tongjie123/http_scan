from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from PyQt5.uic import loadUi

from entity.http.HttpClass import Http
from service.HttpServiceClass import HttpService
from windows.little_windows.SearchWindowClass import SearchWindow
from windows.little_windows.TextBytesWindowClass import TextBytesWindow

"""
日志表格窗口
"""


class LogTableWindow:
    def __init__(self, parent_window):
        self.window = loadUi('ui/log_table.ui')
        
        self.parent_window = parent_window

        """
        表格组件
        """
        self.window.tableWidget: QTableWidget
        # 水平拉伸
        self.window.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 垂直标题隐藏
        self.window.tableWidget.verticalHeader().hide()
        # 设置头部
        self.header_list = ['id', 'host', 'path_query', 'method', '响应状态码', 'send_time', 'wait_time', 'mark']
        self.window.tableWidget.setColumnCount(len(self.header_list))
        self.window.tableWidget.setHorizontalHeaderLabels(self.header_list)
        # 设置path_query列占据较宽空间
        self.window.tableWidget.setColumnWidth(2, 400)
        # 右键菜单
        self.window.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.window.tableWidget.customContextMenuRequested.connect(self.tableWidget_rightMenu)
        # 点击输出报文
        self.window.tableWidget.currentItemChanged.connect(self.tableWidget_currentItemChanged)

        self.window.label: QLabel
        self.window.label.setText('表格总显示行:0，请求字符数:0，响应字符数:0')

        self.req_textBytes_window = TextBytesWindow()
        self.window.frame: QFrame
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.req_textBytes_window.window)
        self.window.frame.setLayout(self.layout)
        self.req_textBytes_window.search_window.set_placeholderText('响应报文')

        self.res_textBytes_window = TextBytesWindow()
        self.window.frame_2: QFrame
        self.layout_2 = QHBoxLayout()
        self.layout_2.addWidget(self.res_textBytes_window.window)
        self.window.frame_2.setLayout(self.layout_2)
        self.res_textBytes_window.search_window.set_placeholderText('响应报文')

        # http服务层对象
        self.httpService = HttpService()

    def tableWidget_rightMenu(self, pos):
        pass

    def tableWidget_currentItemChanged(self, current: QTableWidgetItem, previous: QTableWidgetItem):
        # 清除报文输出文本框
        self.req_textBytes_window.clear()
        self.res_textBytes_window.clear()
        if current is not None:
            # 获取点击的id
            self.tableWidget: QTableWidget
            id_num = int(self.window.tableWidget.item(current.row(), 0).text())
            # 获取请求
            http = self.httpService.select(id_num)
            # 输出报文
            self.req_textBytes_window.search_window.set_text(http.get_req_message())
            if http.status_code != '':
                self.res_textBytes_window.search_window.set_text(http.get_res_message())
        # 输出当前请求的信息
        self.window.label: QLabel
        self.window.tableWidget: QTableWidget
        self.window.label.setText('表格总显示行:%s，请求字符数:%s，响应字符数:%s' % (str(self.window.tableWidget.rowCount()),
                                                                   str(len(
                                                                       self.req_textBytes_window.search_window.get_text())),
                                                                   str(len(
                                                                       self.res_textBytes_window.search_window.get_text()))))
        # 表格聚焦，避免报文搜索带走焦点
        self.window.tableWidget.setFocus()

    def show_http_list(self, http_list: list):
        # 清除数据
        self.window.tableWidget: QTableWidget
        self.window.tableWidget.setRowCount(0)
        # 遍历输出
        for i in range(len(http_list)):
            self.show_http(http_list[i])
            self.parent_window.treeWidget_addItem(http_list[i].u)
        if self.window.tableWidget.rowCount() > 0:
            # 设置选中表格首行，查看报文
            self.window.tableWidget.setCurrentItem(self.window.tableWidget.item(0, 0))

    def show_http(self, http: Http):
        row_count = self.window.tableWidget.rowCount()
        # 末尾插入行
        self.window.tableWidget.insertRow(row_count)
        # 待赋值行的各列值
        # 'id', 'host', 'path_query', 'method', '响应状态码', 'send_time', 'wait_time', 'mark'
        value_list = [http.id, http.u.schema + http.u.hostname + http.u.port, http.u.path + http.u.query,
                      http.method, '', '', '', '']
        if http.status_code != '':
            value_list[4] = http.status_code
        value_list[5] = http.send_time
        value_list[6] = http.wait_time
        value_list[7] = http.mark

        for j in range(len(value_list)):
            self.window.tableWidget.setItem(row_count, j, QTableWidgetItem(str(value_list[j])))

    def tableWidget_setColumns(self, show_column: list):
        self.window.tableWidget: QTableWidget
        for i in range(len(self.header_list)):
            if self.header_list[i] not in show_column:
                self.window.tableWidget.setColumnHidden(i, True)
            else:
                self.window.tableWidget.setColumnHidden(i, False)
