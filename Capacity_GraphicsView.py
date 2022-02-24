# -*- coding: utf-8 -*-
"""
Capacity_GraphicsView.py

Created on Sat Feb 19 16:52:17 2022

@author: Steve D. J.

Copyright (c) 2022 Steve D. J.. All Rights Reserved.
"""

import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene
import pandas as pd
import cv2


class Capacity_GraphicsView(QGraphicsView):
    
    def __init__(self, parent=None):
        super(Capacity_GraphicsView, self).__init__(parent)
        self.update_graph()
    
    def update_graph(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.set_graph)  
        timer.start(1000)
    
    def set_graph(self):
        data = pd.read_excel('data.xlsx', index_col = None, header = 0)
        uFull = int(data.iloc[-1, 9])
        if uFull == 0:
            img=cv2.imread("pictures/condition_00.jpg")          #读取图像
        if uFull == 1:
            img=cv2.imread("pictures/condition_01.jpg")          
        if uFull == 2:
            img=cv2.imread("pictures/condition_02.jpg")          
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)              #转换图像通道
        x = img.shape[1]                                        #获取图像大小
        y = img.shape[0]
        self.zoomscale=1                                        #图片放缩尺度
        frame = QImage(img, x, y, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item=QGraphicsPixmapItem(pix)                      #创建像素图元
        self.scene=QGraphicsScene()                             #创建场景
        self.scene.addItem(self.item)
        self.setScene(self.scene)                  #将场景添加至视图

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Capacity_GraphicsView()
    ui.show()
    sys.exit(app.exec_())
            
