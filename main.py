import sys
from PyQt5.QtWidgets import QApplication


from windows.HomeWindowClass import HomeWindow

"""
程序启动入口
"""

if __name__ == "__main__":
    app = QApplication([])
    # 启动主窗口
    w = HomeWindow()
    sys.exit(app.exec_())
