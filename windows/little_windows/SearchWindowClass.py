from PyQt5.QtWidgets import QPlainTextEdit, QPushButton
from PyQt5.uic import loadUi

"""
搜索组件
"""


class SearchWindow:
    def __init__(self):
        self.window = loadUi('ui/search.ui')
        
        self.window.pushButton: QPushButton
        self.window.pushButton.clicked.connect(self.turn_next)
        self.window.pushButton_2: QPushButton
        self.window.pushButton_2.clicked.connect(self.turn_pre)

    """
    设置占位文本
    """
    def set_placeholderText(self, text: str):
        self.window.plainTextEdit: QPlainTextEdit
        self.window.plainTextEdit.setPlaceholderText(text)

    def append_text(self, text: str):
        self.window.plainTextEdit: QPlainTextEdit
        self.window.plainTextEdit.appendPlainText(text)

    def set_text(self, text: str):
        self.window.plainTextEdit: QPlainTextEdit
        self.window.plainTextEdit.setPlainText(text)

    def get_text(self):
        self.window.plainTextEdit: QPlainTextEdit
        return self.window.plainTextEdit.toPlainText()

    def turn_pre(self):
        self.window.plainTextEdit: QPlainTextEdit
        self.window.plainTextEdit.setPlainText('时间123'.encode('gbk').decode('iso-8859-1').encode('utf-8').__str__())

    def turn_next(self):
        self.window.plainTextEdit: QPlainTextEdit
        s = self.window.plainTextEdit.toPlainText()
        print(s)
    
