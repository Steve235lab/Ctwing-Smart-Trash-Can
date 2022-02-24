# -*- coding: utf-8 -*-
"""
MatplotlibWidget.py

Created on Fri Feb 18 19:50:28 2022

@author: Steve D. J.

Copyright (c) 2022 Steve D. J.. All Rights Reserved.
"""

import sys
import matplotlib
import datetime

matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication,  QVBoxLayout, QSizePolicy, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd


class MyMplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig = Figure(figsize=(width, height), dpi=dpi)  # 新建一个figure
        self.axes = self.fig.add_subplot(111)  # 建立一个子图，如果要建立复合图，可以在这里修改

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    '''启动显示动态图'''
    def Display_dynamic_gantt(self, *args, **kwargs):
        # 设置一个时间对象
        timer = QtCore.QTimer(self)
        # 连接需要动态刷新的方法函数
        timer.timeout.connect(self.update_figure)
        # 表示每1秒钟刷新一次
        timer.start(1000)

    '''绘制动态图方法函数，可以在这里定义自己的绘图逻辑'''
    def update_figure(self):
        self.axes.clear()
        data = pd.read_excel('data.xlsx', index_col = None, header = 0)
        type_ct_list = data.iloc[-1, 5:9].values
        self.axes.bar(('干垃圾', '湿垃圾', '可回收垃圾', '有害垃圾'), type_ct_list)
        #self.axes.set_title('今日各类型垃圾投放次数')
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['top'].set_visible(False)
        self.draw()

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas(self, width=5, height=4, dpi=100)
        # 初始化显示甘特图
        self.mpl.Display_dynamic_gantt()
        self.layout.addWidget(self.mpl)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MatplotlibWidget()
    ui.show()
    sys.exit(app.exec_())

