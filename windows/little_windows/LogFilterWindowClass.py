from PyQt5.QtWidgets import QWidget, QPushButton, QPlainTextEdit, QCheckBox, QLabel, QMessageBox
from PyQt5.uic import loadUi

from service.HttpServiceClass import HttpService


class LogFilterWindow:
    def __init__(self, parent_window):
        self.window = loadUi('ui/log_filter.ui')
        # 父窗口
        self.parent_window = parent_window
        # 默认选中显示过滤按钮
        self.window.checkBox_2: QCheckBox
        self.window.checkBox_2.setChecked(True)
        # 执行按钮
        self.window.pushButton: QPushButton
        self.window.pushButton.clicked.connect(self.execute)

        self.httpService = HttpService()

        self.window.plainTextEdit_2: QPlainTextEdit
        self.window.plainTextEdit_2.setPlainText('select * from tb_http')
        self.window.plainTextEdit_2.setPlaceholderText('select * from tb_http')
        # 标签，提示模糊查询使用
        self.window.label_2: QLabel
        s = '由于底层使用pymysql连接数据库，如果sql语句中包含单独的%字符，会被视为占位符%s，要求提供参数。\n' \
            '因此想要进行模糊查询，可以使用%%表示。示例：where url like "%%baidu.com%%"'
        self.window.label_2.setText(s)

    def execute(self):
        self.window.label: QLabel
        self.window.label.setText('执行中')
        try:
            # 标记过滤
            self.window.checkBox: QCheckBox
            if self.window.checkBox.isChecked():
                self.window.plainTextEdit: QPlainTextEdit
                sql = self.window.plainTextEdit.toPlainText()
                if sql != '':
                    self.httpService.httpDb.baseDb.execute(sql)
            # 显示过滤
            self.window.checkBox_2: QCheckBox
            if self.window.checkBox_2.isChecked():
                self.show_filter()
        except Exception as e:
            QMessageBox.warning(self.window, '警告', '执行异常'+str(e))
        self.window.label.setText('执行结束!!!')

    def show_filter(self):
        self.window.plainTextEdit_2: QPlainTextEdit
        sql = self.window.plainTextEdit_2.toPlainText()
        if sql != '':
            http_list = self.httpService.select_list_bySql(sql)
            self.parent_window.logTable_window.show_http_list(http_list)

    def show_filter_with(self, with_where: str):
        self.window.plainTextEdit_2: QPlainTextEdit
        sql = self.window.plainTextEdit_2.toPlainText()
        if 'where' in sql:
            sql = sql.replace('where', 'where %s and ' % with_where)
            http_list = self.httpService.select_list_bySql(sql)
            self.parent_window.logTable_window.show_http_list(http_list)