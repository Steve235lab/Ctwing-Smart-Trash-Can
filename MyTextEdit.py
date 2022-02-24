# -*- coding: utf-8 -*-
"""
MyTextEdit.py

Created on Sat Feb 19 19:35:10 2022

@author: Steve D. J.

Copyright (c) 2022 Steve D. J.. All Rights Reserved.
"""


import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTextEdit, QApplication
import numpy as np
import pandas as pd
import datetime


class MyTextEdit(QTextEdit):
    
    def __init__(self, parent=None):
        super(QTextEdit, self).__init__(parent)
        self.setReadOnly(True)
        self.update_value()
                
    def update_value(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.set_text)  
        timer.start(1000)
        
    def set_text(self):
        data = pd.read_excel('data.xlsx', index_col = None, header = 0)
        # 显示故障类型与故障上报时间
        fault_type = str(data.iloc[-1, 10])
        fault_type = '\n\n故障类型： ' + fault_type + '\n'
        self.setText(fault_type)
        if fault_type != '\n\n故障类型： healthy\n':
            faultreport_time = str(data.iloc[-1, 11]) + '\n'
            self.append(faultreport_time)
        #self.setStyleSheet("QLabel{color:rgb(22,22,22,255);font-size:10px;font-weight:normal;font-family:Arial;align=center;}")
        # 显示最新消息
        f = open('info_cache.txt', 'r')
        info_cache = f.read()
        f.close()
        info_cache = '最新消息：\n' + info_cache + '\n'
        self.append(info_cache)
        # 显示重启上报时间、换桶时间以及每日上报时间
        try:
            restarttime = '重启时间： ' + str(data.iloc[-1, 12]) + '\n'
            self.append(restarttime)
            uptime = '换桶时间： ' + str(data.iloc[-1, 13]) + '\n'
            self.append(uptime)
            oneday_time = '每日上报时间： ' + str(data.iloc[-1, 16]) + '\n'
            self.append(oneday_time)
        except:
            pass
        # 显示经纬度
        Longitude = '经度： ' + str(data.iloc[-1, 17]) + '\n'
        Latitude = '纬度： ' + str(data.iloc[-1, 18]) + '\n'
        self.append(Longitude)
        self.append(Latitude)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = QTextEdit()
    ui.show()
    sys.exit(app.exec_())
