# -*- coding: utf-8 -*-
"""
Variable_QLabel.py

Created on Sat Feb 19 14:40:14 2022

@author: Steve D. J.

Copyright (c) 2022 Steve D. J.. All Rights Reserved.
"""


import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QApplication
import pandas as pd


class Variable_QLabel(QLabel):
    
    def __init__(self, parent=None):
        super(Variable_QLabel, self).__init__(parent)
        self.update_value()
                
    def update_value(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.set_text)  
        timer.start(1000)
        
    def set_text(self):
        data = pd.read_excel('data.xlsx', index_col = None, header = 0)
        daily_cnt = 0
        try:
            for i in range(5, 9):
                daily_cnt = daily_cnt + int(data.iloc[-1, i])
        except:
            pass
        daily_cnt_str = ' ' + str(daily_cnt)
        self.setText(daily_cnt_str)
        self.setStyleSheet("QLabel{color:rgb(6, 6, 6, 150);font-size:180px;font-weight:normal;font-family:Arial;align=center;}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Variable_QLabel()
    ui.show()
    sys.exit(app.exec_())
