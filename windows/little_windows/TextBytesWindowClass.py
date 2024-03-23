from PyQt5.QtWidgets import QTabWidget, QPlainTextEdit
from PyQt5.uic import loadUi

from windows.little_windows.SearchWindowClass import SearchWindow

"""
文本字节窗口
"""


class TextBytesWindow:
    def __init__(self):
        self.window = loadUi('ui/text_bytes.ui')

        self.search_window = SearchWindow()
        self.window.tabWidget: QTabWidget
        self.window.tabWidget.insertTab(0, self.search_window.window, '文本')
        self.window.tabWidget.removeTab(1)
        self.window.tabWidget.setTabText(1, '字节')
        self.window.tabWidget.setCurrentIndex(0)

    def clear(self):
        self.search_window.set_text('')
        self.window.plainTextEdit: QPlainTextEdit
        self.window.plainTextEdit.setPlainText('')
        self.window.plainTextEdit_2: QPlainTextEdit
        self.window.plainTextEdit_2.setPlainText('')
