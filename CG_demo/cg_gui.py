#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import math
import cg_algorithms as alg

import numpy as np
from PIL import Image
import os

from typing import Optional
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QStyleOptionGraphicsItem,
    QInputDialog,
    QColorDialog,
    QFileDialog
    )
from PyQt5.QtGui import QPainter, QMouseEvent, QColor
from PyQt5.QtCore import QRectF


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """
    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None
        
        self.R = 0
        self.G = 0
        self.B = 0
        
        self.translate_delta = [[0, 0], [0, 0]]
        self.rotate_delta = [[-1, -1], [-1, -1], [-1, -1]]
        self.clip_delta = [[0, 0], [0, 0]]
        self.p_list = []
        
        #self.degree = 0
        #self.clip_id = ''
        
    def clear(self):
        self.item_dict.clear()
        self.selected_id = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None
        self.status = ''
        
        self.R = 0
        self.G = 0
        self.B = 0
        
    def setColor(self, r, g, b):
        self.R = r
        self.G = g
        self.B = b
        
    def start_save_canvas(self):
        '''
        imgFile = QFileDialog.getSaveFileName(self, "保存图像", './', "图像 (*.png)")[0]
        if imgFile:
            img = pixmap.save(imgFile)
        '''
        height = self.height()
        width = self.width()
        canvas = np.zeros([height, width, 3], np.uint8)
        canvas.fill(255)
        color = np.zeros(3, np.uint8)
        for temp_id in self.item_dict.keys():
            if self.item_dict[temp_id] != None:
                if self.item_dict[temp_id].item_type != None:
                    color[0] = self.item_dict[temp_id].R
                    color[1] = self.item_dict[temp_id].G
                    color[2] = self.item_dict[temp_id].B
                    if self.item_dict[temp_id].item_type == 'line':
                        pixels = alg.draw_line(self.item_dict[temp_id].p_list, self.item_dict[temp_id].algorithm)
                        for x, y in pixels:
                            canvas[y, x] = color
                    elif self.item_dict[temp_id].item_type == 'polygon':
                        pixels = alg.draw_polygon(self.item_dict[temp_id].p_list, self.item_dict[temp_id].algorithm)
                        for x, y in pixels:
                            canvas[y, x] = color
                    elif self.item_dict[temp_id].item_type == 'circle':
                        temp_list = [[0, 0], [0, 0]]
                        x0, y0 = self.item_dict[temp_id].p_list[0]  #圆心
                        x1, y1 = self.item_dict[temp_id].p_list[1]
                        r = math.sqrt((x0-x1) ** 2 + (y0-y1) ** 2)
                        temp_list = [[0, 0], [0, 0]]
                        temp_list[0] = [x0 - r, y0 - r]
                        temp_list[1] = [x0 + r, y0 + r]
                        pixels = alg.draw_ellipse(temp_list)
                        for x, y in pixels:
                            canvas[y, x] = color
                    elif self.item_dict[temp_id].item_type == 'ellipse':
                        pixels = alg.draw_ellipse(self.item_dict[temp_id].p_list)
                        for x, y in pixels:
                            canvas[y, x] = color
                    elif self.item_dict[temp_id].item_type == 'curve':
                        pixels = alg.draw_curve(self.item_dict[temp_id].p_list, self.item_dict[temp_id].algorithm)
                        for x, y in pixels:
                            canvas[y, x] = color
        save_name = QFileDialog.getSaveFileName(self, "保存图像", './', "图像 (*.bmp)")[0]
        Image.fromarray(canvas).save(os.path.join('./', save_name), 'bmp')
        
        
    def start_draw_line(self, algorithm, item_id):
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        
    def start_draw_polygon(self, algorithm, item_id):
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
    
    def start_draw_circle(self, algorithm, item_id):
        self.status = 'circle'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
    
    def start_draw_ellipse(self, algorithm, item_id):
        self.status = 'ellipse'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        
        
    def start_draw_curve(self, algorithm, item_id):
        self.status = 'curve'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        
    def start_draw_custom(self, algorithm, item_id):
        self.status = 'custom'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def finish_draw(self):
        self.temp_item = None
        self.temp_id = self.main_window.get_id()

    def clear_selection(self):
        if self.selected_id != '':
            if self.status != 'translate' and self.status != 'rotate' and self.status != 'clip' and self.status != 'scale':
                self.item_dict[self.selected_id].selected = False
                self.selected_id = ''
            
    def selection_changed(self, selected):
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.status = ''
        self.updateScene([self.sceneRect()])
        
    def start_translate(self):
        self.status = 'translate'
        self.translate_delta = [[0, 0], [0, 0]]
        if self.selected_id != '':
            for i in range(len(self.item_dict[self.selected_id].p_list)):
                temp = self.item_dict[self.selected_id].p_list[i].copy()
                self.p_list.append(temp)
    
    def start_rotate(self):
        self.status = 'rotate'
        self.rotate_delta = [[-1, -1], [-1, -1], [-1, -1]]
        if self.selected_id != '':
            for i in range(len(self.item_dict[self.selected_id].p_list)):
                temp = self.item_dict[self.selected_id].p_list[i].copy()
                self.p_list.append(temp)

    def start_clip(self, algorithm):
        self.status = 'clip'
        self.temp_algorithm = algorithm
        self.clip_delta = [[0, 0], [0, 0]]
        if self.selected_id != '':
            if self.item_dict[self.selected_id].item_type == 'line':
                for i in range(len(self.item_dict[self.selected_id].p_list)):
                    temp = self.item_dict[self.selected_id].p_list[i].copy()
                    self.p_list.append(temp)

    def start_scale(self):
        self.status = 'scale'
        if self.selected_id != '':
            for i in range(len(self.item_dict[self.selected_id].p_list)):
                temp = self.item_dict[self.selected_id].p_list[i].copy()
                self.p_list.append(temp)
        

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            #self.temp_id = str(int(self.temp_id) + 1)
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.R, self.G, self.B)
            self.scene().addItem(self.temp_item)
       
        elif self.status == 'polygon':
            if self.temp_item == None:
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y]], self.temp_algorithm, self.R, self.G, self.B)
                self.scene().addItem(self.temp_item)
                self.list_widget.addItem(self.temp_id)
            else:
                self.temp_item.p_list.append([x, y])
        
        elif self.status == 'circle':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.R, self.G, self.B)
            self.scene().addItem(self.temp_item)
        
        elif self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.R, self.G, self.B)
            self.scene().addItem(self.temp_item)
        
        elif self.status == 'curve':
            #print('click')
            if self.temp_item == None:  
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y]], self.temp_algorithm, self.R, self.G, self.B)
                self.scene().addItem(self.temp_item)
                self.list_widget.addItem(self.temp_id)
            else:
                self.temp_item.p_list.append([x, y])
        
        elif self.status == 'custom':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y]], self.temp_algorithm, self.R, self.G, self.B)
            self.scene().addItem(self.temp_item)
        
        elif self.status == 'translate':
            '''
            if self.selected_id != '':
                self.p_list = self.item_dict[self.selected_id].p_list
            '''
            self.translate_delta[0][0] = x
            self.translate_delta[0][1] = y
            #print(x, y)
            
        elif self.status == 'rotate':  #旋转中心
            if self.selected_id != '':
                if self.rotate_delta[0][0] == -1:
                    self.rotate_delta[0][0] = x
                    self.rotate_delta[0][1] = y
                    self.rotate_delta[1][1] = y
                elif self.rotate_delta[1][0] == -1:
                    self.rotate_delta[1][0] = self.rotate_delta[0][0] + 100
        
        elif self.status == 'clip':
            #print(x, y)
            
            if self.selected_id != '':
                if self.item_dict[self.selected_id].item_type == 'line':
                    self.clip_delta[0][0] = x
                    self.clip_delta[0][1] = y
           
        elif self.status == 'scale':
            if self.selected_id != '':
                s = QInputDialog.getDouble(self, '请输入缩放倍数', '倍数', 1.0, 0.01, 100)[0]
                temp = []
                for i in range(len(self.p_list)):
                    t = self.p_list[i].copy()
                    temp.append(t)
                self.item_dict[self.selected_id].p_list = alg.scale(temp, x, y, s)
                self.status = None
                self.p_list.clear()
                
        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'polygon':
            if self.temp_item != None:
                if self.temp_id == self.temp_item.id:
                    self.temp_item.p_list[-1] = [x, y]
        elif self.status == 'circle':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'curve':
            if self.temp_item != None:
                if self.temp_id == self.temp_item.id:
                    self.temp_item.p_list[-1] = [x, y]
        elif self.status == 'custom':
            if self.temp_item != None:
                if self.temp_id == self.temp_item.id:
                    self.temp_item.p_list.append([x, y])
                    
        elif self.status == 'translate':
            if self.selected_id != '':
                #print('delta', self.translate_delta)
                self.translate_delta[1][0] = x
                self.translate_delta[1][1] = y
                temp = []
                for i in range(len(self.p_list)):
                    t = self.p_list[i].copy()
                    temp.append(t)
                self.item_dict[self.selected_id].p_list = alg.translate(temp, self.translate_delta[1][0] - self.translate_delta[0][0], self.translate_delta[1][1] - self.translate_delta[0][1])
                #print('self', self.p_list)
                #print('point', self.item_dict[self.selected_id].p_list)
        
        elif self.status == 'rotate':
            if self.selected_id != '':
                if self.rotate_delta[1][0] == -1:
                    pass
                #elif self.rotate_delta[2][0] == -1:
                else:
                    self.rotate_delta[2][0] = x
                    self.rotate_delta[2][1] = y
                    temp = []
                    for i in range(len(self.p_list)):
                        t = self.p_list[i].copy()
                        temp.append(t)
                    a = math.sqrt((self.rotate_delta[0][0]-self.rotate_delta[1][0]) ** 2 + (self.rotate_delta[0][1]-self.rotate_delta[1][1]) ** 2)
                    b = math.sqrt((self.rotate_delta[0][0]-self.rotate_delta[2][0]) ** 2 + (self.rotate_delta[0][1]-self.rotate_delta[2][1]) ** 2)
                    c = math.sqrt((self.rotate_delta[1][0]-self.rotate_delta[2][0]) ** 2 + (self.rotate_delta[1][1]-self.rotate_delta[2][1]) ** 2)
                    cosr = 1
                    if a != 0 and b != 0:
                        cosr = (a*a + b*b - c*c ) / (2*a*b)
                    r = math.acos(cosr)
                    if self.rotate_delta[2][1] > self.rotate_delta[0][1]:
                        degree = -float(math.degrees(r))
                    else:
                        degree = float(math.degrees(r))
                    #print(degree)
                    self.item_dict[self.selected_id].p_list = alg.rotate(temp, self.rotate_delta[0][0], self.rotate_delta[0][1], degree)

        elif self.status == 'clip':
            if self.selected_id != '':
                if self.item_dict[self.selected_id].item_type == 'line':
                    self.clip_delta[1][0] = x
                    self.clip_delta[1][1] = y
                    temp = []
                    for i in range(len(self.p_list)):
                        t = self.p_list[i].copy()
                        temp.append(t)           
                    '''
                    temp_polygon = []
                    temp_polygon.append([self.clip_delta[0][0],self.clip_delta[0][1]])
                    temp_polygon.append([self.clip_delta[1][0],self.clip_delta[0][1]])
                    temp_polygon.append([self.clip_delta[1][0],self.clip_delta[1][1]])
                    temp_polygon.append([self.clip_delta[0][0],self.clip_delta[1][1]])
                    print(temp_polygon)
                    self.clip_id = '2147483647'
                    temp_item = MyItem(self.clip_id, 'polygon', temp_polygon, 'DDA', self.R, self.G, self.B)
                    self.scene().addItem(temp_item)
                    self.item_dict[self.clip_id] = temp_item
                    '''
                    self.item_dict[self.selected_id].p_list = alg.clip(temp, self.clip_delta[0][0], self.clip_delta[0][1], self.clip_delta[1][0], self.clip_delta[1][1], self.temp_algorithm)

        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status == 'line':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
            
        elif self.status == 'polygon':
            self.item_dict[self.temp_id] = self.temp_item
            #self.list_widget.addItem(self.temp_id)
            
        elif self.status == 'circle':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        
        elif self.status == 'ellipse':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
            
        elif self.status == 'curve':
            self.item_dict[self.temp_id] = self.temp_item
            
        elif self.status == 'custom':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        
        elif self.status == 'translate':
            self.translate_delta = [[0, 0], [0, 0]]
            self.status = None
            self.p_list.clear()
            
        elif self.status == 'rotate':
            if self.selected_id != '':
                if self.rotate_delta[2][0] != -1:        
                    self.status == None
                    self.rotate_delta = [[-1, -1], [-1, -1], [-1, -1]]
                    self.p_list.clear()
        
        elif self.status == 'clip':
            '''
            if self.clip_id != '':
                self.item_dict.pop(self.clip_id)
                self.clip_id = ''
            '''
            self.clip_delta = [[0, 0], [0, 0]]
            self.status = None
            self.p_list.clear()
        
        super().mouseReleaseEvent(event)
        
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        #print('doubleclick')
        if self.status == 'polygon':
            #del(self.temp_item.p_list[-1])
            self.finish_draw()
        elif self.status == 'curve':
            #del(self.temp_item.p_list[-1])
            self.finish_draw()
        
            


class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """
    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '', r = 0, g = 0, b = 0, parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id           # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list        # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False
        
        self.R = r
        self.G = g
        self.B = b


    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        painter.setPen(QColor(self.R, self.G, self.B))
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(0, 0, 255))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'polygon':
            item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(0, 0, 255))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'circle':
            x0, y0 = self.p_list[0]  #圆心
            x1, y1 = self.p_list[1]
            r = math.sqrt((x0-x1) ** 2 + (y0-y1) ** 2)
            temp_list = [[0, 0], [0, 0]]
            temp_list[0] = [x0 - r, y0 - r]
            temp_list[1] = [x0 + r, y0 + r]
            item_pixels = alg.draw_ellipse(temp_list)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(0, 0, 255))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(0, 0, 255))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(0, 0, 255))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'custom':
            for p in self.p_list:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(0, 0, 255))
                painter.drawRect(self.boundingRect())
    def boundingRect(self) -> QRectF:
        if self.item_type == 'line':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'polygon':
            x_max = 0
            y_max = 0
            x_min = 2000
            y_min = 2000
            for i in range(len(self.p_list)):
                if self.p_list[i][0] > x_max:
                    x_max = self.p_list[i][0]
                if self.p_list[i][0] < x_min:
                    x_min = self.p_list[i][0]
                if self.p_list[i][1] > y_max:
                    y_max = self.p_list[i][1]
                if self.p_list[i][1] < y_min:
                    y_min = self.p_list[i][1]
            return QRectF(x_min - 1, y_min - 1, x_max - x_min + 2, y_max - y_min + 2)
        elif self.item_type == 'circle':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            r = math.sqrt((x0-x1) ** 2 + (y0-y1) ** 2)
            return QRectF(x0 - r - 1, y0 - r - 1, r * 2 + 2, r * 2 + 2)
        elif self.item_type == 'ellipse':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'curve':
            x_max = 0
            y_max = 0
            x_min = 2000
            y_min = 2000
            for i in range(len(self.p_list)):
                if self.p_list[i][0] > x_max:
                    x_max = self.p_list[i][0]
                if self.p_list[i][0] < x_min:
                    x_min = self.p_list[i][0]
                if self.p_list[i][1] > y_max:
                    y_max = self.p_list[i][1]
                if self.p_list[i][1] < y_min:
                    y_min = self.p_list[i][1]
            return QRectF(x_min - 1, y_min - 1, x_max - x_min + 2, y_max - y_min + 2)
        elif self.item_type == 'custom':
            x_max = 0
            y_max = 0
            x_min = 2000
            y_min = 2000
            for i in range(len(self.p_list)):
                if self.p_list[i][0] > x_max:
                    x_max = self.p_list[i][0]
                if self.p_list[i][0] < x_min:
                    x_min = self.p_list[i][0]
                if self.p_list[i][1] > y_max:
                    y_max = self.p_list[i][1]
                if self.p_list[i][1] < y_min:
                    y_min = self.p_list[i][1]
            return QRectF(x_min - 1, y_min - 1, x_max - x_min + 2, y_max - y_min + 2)

class MainWindow(QMainWindow):
    """
    主窗口类
    """
    def __init__(self):
        super().__init__()
        self.item_cnt = 0
        
        #重置画布时的宽和高
        self.width = 600
        self.height = 600
        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        save_canvas_act = file_menu.addAction('保存画布')
        exit_act = file_menu.addAction('退出')
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        circle_act = draw_menu.addAction('圆')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        custom_act = draw_menu.addAction('手动画图')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')

        # 连接信号和槽函数
        set_pen_act.triggered.connect(self.set_pen_action)
        reset_canvas_act.triggered.connect(self.reset_canvas_action)
        exit_act.triggered.connect(qApp.quit)
        save_canvas_act.triggered.connect(self.save_canvas_action)
        
        line_naive_act.triggered.connect(self.line_naive_action)
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)
        
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        
        circle_act.triggered.connect(self.circle_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        custom_act.triggered.connect(self.custom_action)
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
        clip_cohen_sutherland_act.triggered.connect(self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG Demo')

    def get_id(self):
        _id = str(self.item_cnt)
        if _id in self.canvas_widget.item_dict.keys():
            if self.canvas_widget.item_dict[_id] != None:
                if self.canvas_widget.item_dict[_id].item_type != None:
                    self.item_cnt += 1
        _id = str(self.item_cnt)
        return _id
    
    def set_id(self, cnt):
        self.item_cnt = cnt
        
    
    def reset_canvas_action(self):
        #getInt返回tuple
        self.width = QInputDialog.getInt(self, '请输入重置后长度', '长度', 600, 100, 1000)[0]
        self.height = QInputDialog.getInt(self, '请输入重置后高度', '高度', 600, 100, 1000)[0]
        
        self.scene.setSceneRect(0, 0, self.width, self.height)
        self.canvas_widget.setFixedSize(self.width, self.height)
        self.resize(self.width, self.height)
        
        self.item_cnt = 0
        self.scene.clear()
        self.list_widget.clear()
        self.canvas_widget.clear()
        
    def save_canvas_action(self):
        self.canvas_widget.start_save_canvas()
        
    def set_pen_action(self):
        '''
        R = QInputDialog.getInt(self, '请输入R', 'Red', 0, 0, 255)[0]
        G = QInputDialog.getInt(self, '请输入R', 'Green', 0, 0, 255)[0]
        B = QInputDialog.getInt(self, '请输入R', 'Blue', 0, 0, 255)[0]
        '''
        self.statusBar().showMessage('设置画笔颜色')
        color = QColorDialog.getColor(title = '颜色')
        self.canvas_widget.setColor(color.red(), color.green(), color.blue())

    def line_naive_action(self):
        self.canvas_widget.start_draw_line('Naive', self.get_id())
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        
    def line_dda_action(self):
        self.canvas_widget.start_draw_line('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        
    def line_bresenham_action(self):
        self.canvas_widget.start_draw_line('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        
    def polygon_dda_action(self):
        self.canvas_widget.start_draw_polygon('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        
    def polygon_bresenham_action(self):
        self.canvas_widget.start_draw_polygon('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制多边形')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        
    def ellipse_action(self):
        self.canvas_widget.start_draw_ellipse('Midpoint_circle', self.get_id())
        self.statusBar().showMessage('中点圆生成算法绘制椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
     
    def circle_action(self):
        self.canvas_widget.start_draw_circle('Midpoint_circle', self.get_id())
        self.statusBar().showMessage('中点圆生成算法绘制圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
     
    def curve_bezier_action(self):
        self.canvas_widget.start_draw_curve('Bezier', self.get_id())
        self.statusBar().showMessage('Bezier算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def curve_b_spline_action(self):
        self.canvas_widget.start_draw_curve('B-spline', self.get_id())
        self.statusBar().showMessage('B-spline算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        
    def custom_action(self):
        self.canvas_widget.start_draw_custom('None', self.get_id())
        self.statusBar().showMessage('手画图像')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def translate_action(self):
        self.canvas_widget.start_translate()
        self.statusBar().showMessage('平移变换')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        
    def rotate_action(self):
        self.canvas_widget.start_rotate()
        self.statusBar().showMessage('旋转变换')
        
    def scale_action(self):
        self.canvas_widget.start_scale()
        self.statusBar().showMessage('缩放变换')
        
    def clip_cohen_sutherland_action(self):
        self.canvas_widget.start_clip('Cohen-Sutherland')
        self.statusBar().showMessage('线段裁剪-Cohen-Sutherland')
        
    def clip_liang_barsky_action(self):
        self.canvas_widget.start_clip('Liang-Barsky')
        self.statusBar().showMessage('线段裁剪-Liang-Barsky')
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
