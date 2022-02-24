from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import os


# 建立图形窗口
Form, Window = uic.loadUiType("MainWindow.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()
app.exec_()
    
