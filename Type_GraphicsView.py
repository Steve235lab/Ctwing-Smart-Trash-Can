# -*- coding: utf-8 -*-
"""
Type_GraphicsView.py

Created on Sat Feb 19 19:08:07 2022

@author: Steve D. J.

Copyright (c) 2022 Steve D. J.. All Rights Reserved.
"""


import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene
import pandas as pd
import cv2


class Type_GraphicsView(QGraphicsView):
    
    def __init__(self, parent=None):
        super(Type_GraphicsView, self).__init__(parent)
        self.update_graph()
    
    def update_graph(self):
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.set_graph)  
        timer.start(1000)
    
    def set_graph(self):
        data = pd.read_excel('data.xlsx', index_col = None, header = 0)
        present_type = int(data.iloc[-1, 4])
        if present_type == 1:
            img=cv2.imread("pictures/type_res.jpg")          #读取图像
        if present_type == 2:
            img=cv2.imread("pictures/type_hf.jpg")          
        if present_type == 3:
            img=cv2.imread("pictures/type_rec.jpg")          
        if present_type == 4:
            img=cv2.imread("pictures/type_haz.jpg")          
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
    ui = Type_GraphicsView()
    ui.show()
    sys.exit(app.exec_())
