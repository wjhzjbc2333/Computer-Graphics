#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 本文件只允许依赖math库
import math


def draw_line(p_list, algorithm):
    """绘制线段

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'，此处的'Naive'仅作为示例，测试时不会出现
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    result = []
    if algorithm == 'Naive':
        if x0 == x1:
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            for x in range(x0, x1 + 1):
                result.append((x, int(y0 + k * (x - x0))))
    elif algorithm == 'DDA':
        if x0 == x1:
            if y0 > y1:
                y0, y1 = y1, y0
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0) 
            if k > 1:
                for y in range(y0, y1 + 1):
                    result.append((int(x0 + 1 / k * (y - y0)), y))
            elif k <= 1 and k >= 0:
                for x in range(x0, x1 + 1):
                    result.append((x, int(y0 + k * (x - x0))))
            elif k < -1:
                for y in range(y1, y0 + 1):
                    result.append((int(x0 + 1 / k * (y - y0)), y))
            elif k >= -1 and k < 0:
                for x in range(x0, x1 + 1):
                    result.append((x, int(y0 + k * (x - x0))))         
    elif algorithm == 'Bresenham':
        if x0 == x1:
            if y0 > y1:
                y0, y1 = y1, y0
            for y in range(y0, y1 + 1):
                result.append((x0, y))
        else:
            if x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            k = (y1 - y0) / (x1 - x0)
            if k <= 1 and k >= 0:
                p = 2 * k - 1
                delta_y = k
                adder = 0
                result.append((x0, y0))
                for x in range(x0 + 1, x1 + 1):
                    if p < 0:
                        result.append((x, y0 + adder))
                        p = p + 2 * delta_y
                    else:
                        adder += 1
                        result.append((x, y0 + adder))
                        p = p - 2 + 2 * delta_y 
            elif k > 1:
                p = 2 * 1 / k - 1
                delta_x = 1 / k
                adder = 0
                result.append((x0, y0))
                for y in range(y0 + 1, y1 + 1):
                    if p < 0:
                        result.append((x0 + adder, y))
                        p = p + 2 * delta_x
                    else:
                        adder += 1
                        result.append((x0 + adder, y))
                        p = p - 2 + 2 * delta_x
            elif k < 0 and k >= -1:
                p = 2 * (-k) - 1
                delta_y = -k
                adder = 0
                result.append((x0, y0))
                for x in range(x0 + 1, x1 + 1):
                    if p < 0:
                        result.append((x, y0 - adder))
                        p = p + 2 * delta_y
                    else:
                        adder += 1
                        result.append((x, y0 - adder))
                        p = p - 2 + 2 * delta_y 
            elif k < -1:
                p = 2 * (-1 / k) - 1
                delta_x = -1 / k
                adder = 0
                result.append((x1, y1))
                for y in range(y1 + 1, y0 + 1):
                    if p < 0:
                        result.append((x1 - adder, y))
                        p = p + 2 * delta_x
                    else:
                        adder += 1
                        result.append((x1 - adder, y))
                        p = p - 2 + 2 * delta_x
    return result


def draw_polygon(p_list, algorithm):
    """绘制多边形

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 多边形的顶点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'DDA'和'Bresenham'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    for i in range(len(p_list)):
        line = draw_line([p_list[i - 1], p_list[i]], algorithm)
        result += line
    return result


def draw_ellipse(p_list):
    """绘制椭圆（采用中点圆生成算法）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 椭圆的矩形包围框左上角和右下角顶点坐标
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    x0, y0 = p_list[0]
    x1, y1 = p_list[1]
    '''
    line = draw_line([p_list[0], p_list[1]], 'DDA')
    result += line
    '''
    if x0 > x1:
        x0, x1 = x1, x0
    if y0 > y1:
        y0, y1 = y1, y0
    midpoint_x = (x0 + x1) / 2
    midpoint_y = (y0 + y1) / 2
    Rx = abs((x1 - x0) / 2)
    Ry = abs((y1 - y0) / 2)
    P1 = 0   #abs(切线斜率) <= 1
    P2 = 0   #abs(切线斜率) > 1
    x = 0
    y = Ry
    if Rx > Ry:
        result.append((midpoint_x, midpoint_y + y))
        result.append((midpoint_x, midpoint_y - y))
        result.append((midpoint_x + Rx, midpoint_y))
        result.append((midpoint_x - Rx, midpoint_y))
        P1 = Ry * Ry - Rx * Rx * Ry + Rx * Rx / 4
        while Ry * Ry * x < Rx * Rx * y:
            if P1 < 0:
                P1 = P1 + 2 * Ry * Ry * x + 3 * Ry * Ry
                x += 1
                result.append((midpoint_x + x, midpoint_y + y))
                result.append((midpoint_x + x, midpoint_y - y))
                result.append((midpoint_x - x, midpoint_y + y))
                result.append((midpoint_x - x, midpoint_y - y))
            else:
                P1 = P1 + 2 * Ry * Ry * x - 2 * Rx * Rx * y + 2 * Rx * Rx + 3 * Ry * Ry
                x += 1
                y -= 1
                result.append((midpoint_x + x, midpoint_y + y))
                result.append((midpoint_x + x, midpoint_y - y))
                result.append((midpoint_x - x, midpoint_y + y))
                result.append((midpoint_x - x, midpoint_y - y))
        P2 = Ry * Ry * (x + 0.5)*(x + 0.5) + Rx * Rx * (y - 1) * (y - 1) - Rx * Rx * Ry * Ry
        while y > 0:
            if P2 <= 0:
                P2 = P2 + 2 * Ry * Ry * (x + 1) + Rx * Rx * (3 - 2 * y)
                y -= 1
                x += 1
                result.append((midpoint_x + x, midpoint_y + y))
                result.append((midpoint_x + x, midpoint_y - y))
                result.append((midpoint_x - x, midpoint_y + y))
                result.append((midpoint_x - x, midpoint_y - y))
            else:
                P2 = P2 + Rx * Rx * (3 - 2 * y)
                y -= 1
                result.append((midpoint_x + x, midpoint_y + y))
                result.append((midpoint_x + x, midpoint_y - y))
                result.append((midpoint_x - x, midpoint_y + y))
                result.append((midpoint_x - x, midpoint_y - y))
    else:
        x = Rx
        y = 0
        result.append((midpoint_x, midpoint_y + Ry))
        result.append((midpoint_x, midpoint_y - Ry))
        result.append((midpoint_x + Rx, midpoint_y))
        result.append((midpoint_x - Rx, midpoint_y))
        P1 = Rx * Rx - Ry * Ry * Rx + Ry * Ry / 4
        while Rx * Rx * y < Ry * Ry * x:
            if P1 < 0:
                P1 = P1 + 2 * Rx * Rx * y + 3 * Rx * Rx
                y += 1
                result.append((midpoint_x + x, midpoint_y + y))
                result.append((midpoint_x + x, midpoint_y - y))
                result.append((midpoint_x - x, midpoint_y + y))
                result.append((midpoint_x - x, midpoint_y - y))
            else:
                P1 = P1 + 2 * Rx * Rx * y - 2 * Ry * Ry * x + 2 * Ry * Ry + 3 * Rx * Rx
                y += 1
                x -= 1
                result.append((midpoint_x + x, midpoint_y + y))
                result.append((midpoint_x + x, midpoint_y - y))
                result.append((midpoint_x - x, midpoint_y + y))
                result.append((midpoint_x - x, midpoint_y - y))
        P2 = Rx * Rx * (y + 0.5)*(y + 0.5) + Ry * Ry * (x - 1) * (x - 1) - Rx * Rx * Ry * Ry
        while x > 0:
            if P2 <= 0:
                P2 = P2 + 2 * Rx * Rx * (y + 1) + Ry * Ry * (3 - 2 * x)
                x -= 1
                y += 1
                result.append((midpoint_x + x, midpoint_y + y))
                result.append((midpoint_x + x, midpoint_y - y))
                result.append((midpoint_x - x, midpoint_y + y))
                result.append((midpoint_x - x, midpoint_y - y))
            else:
                P2 = P2 + Ry * Ry * (3 - 2 * x)
                x -= 1
                result.append((midpoint_x + x, midpoint_y + y))
                result.append((midpoint_x + x, midpoint_y - y))
                result.append((midpoint_x - x, midpoint_y + y))
                result.append((midpoint_x - x, midpoint_y - y))
    
    return result


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    if algorithm == 'Bezier':
        pass
    
    elif algorithm == 'B-spline':
        pass
    pass


def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    for i in range(len(p_list)):
        p_list[i][0] += dx
        p_list[i][1] += dy
    return p_list


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = []
    for i in range(len(p_list)):
        p_list[i][0] -= x
        p_list[i][1] -= y
        temp_x = p_list[i][0]
        temp_y = p_list[i][1]
        p_list[i][0] = temp_x * math.cos((360 - r) / 180 * math.pi) - temp_y * math.sin((360 - r) / 180 * math.pi)
        p_list[i][1] = temp_x * math.sin((360 - r) / 180 * math.pi) + temp_y * math.cos((360 - r) / 180 * math.pi)
        p_list[i][0] += x;
        p_list[i][1] += y
        
    return result


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    pass


def clip(p_list, x_min, y_min, x_max, y_max, algorithm):
    """线段裁剪

    :param p_list: (list of list of int: [[x0, y0], [x1, y1]]) 线段的起点和终点坐标
    :param x_min: 裁剪窗口左上角x坐标
    :param y_min: 裁剪窗口左上角y坐标
    :param x_max: 裁剪窗口右下角x坐标
    :param y_max: 裁剪窗口右下角y坐标
    :param algorithm: (string) 使用的裁剪算法，包括'Cohen-Sutherland'和'Liang-Barsky'
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1]]) 裁剪后线段的起点和终点坐标
    """
    if algorithm == 'Cohen-Sutherland':
        pass
    elif algorithm == 'Liang-Barsky':
        pass
    pass
    
