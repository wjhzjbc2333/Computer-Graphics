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
    #print(p_list)
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
    midpoint_x = int((x0 + x1) / 2)
    midpoint_y = int((y0 + y1) / 2)
    Rx = int(abs((x1 - x0) / 2))
    Ry = int(abs((y1 - y0) / 2))
    P1 = 0   #abs(切线斜率) <= 1
    P2 = 0   #abs(切线斜率) > 1
    x = 0
    y = Ry
    if Rx > Ry:
        result.append([midpoint_x, midpoint_y + y])
        result.append([midpoint_x, midpoint_y - y])
        result.append([midpoint_x + Rx, midpoint_y])
        result.append([midpoint_x - Rx, midpoint_y])
        P1 = Ry * Ry - Rx * Rx * Ry + Rx * Rx / 4
        while Ry * Ry * x < Rx * Rx * y:
            if P1 < 0:
                P1 = P1 + 2 * Ry * Ry * x + 3 * Ry * Ry
                x += 1
                result.append([midpoint_x + x, midpoint_y + y])
                result.append([midpoint_x + x, midpoint_y - y])
                result.append([midpoint_x - x, midpoint_y + y])
                result.append([midpoint_x - x, midpoint_y - y])
            else:
                P1 = P1 + 2 * Ry * Ry * x - 2 * Rx * Rx * y + 2 * Rx * Rx + 3 * Ry * Ry
                x += 1
                y -= 1
                result.append([midpoint_x + x, midpoint_y + y])
                result.append([midpoint_x + x, midpoint_y - y])
                result.append([midpoint_x - x, midpoint_y + y])
                result.append([midpoint_x - x, midpoint_y - y])
        P2 = Ry * Ry * (x + 0.5)*(x + 0.5) + Rx * Rx * (y - 1) * (y - 1) - Rx * Rx * Ry * Ry
        while y > 0:
            if P2 <= 0:
                P2 = P2 + 2 * Ry * Ry * (x + 1) + Rx * Rx * (3 - 2 * y)
                y -= 1
                x += 1
                result.append([midpoint_x + x, midpoint_y + y])
                result.append([midpoint_x + x, midpoint_y - y])
                result.append([midpoint_x - x, midpoint_y + y])
                result.append([midpoint_x - x, midpoint_y - y])
            else:
                P2 = P2 + Rx * Rx * (3 - 2 * y)
                y -= 1
                result.append([midpoint_x + x, midpoint_y + y])
                result.append([midpoint_x + x, midpoint_y - y])
                result.append([midpoint_x - x, midpoint_y + y])
                result.append([midpoint_x - x, midpoint_y - y])
    else:
        x = Rx
        y = 0
        result.append([midpoint_x, midpoint_y + Ry])
        result.append([midpoint_x, midpoint_y - Ry])
        result.append([midpoint_x + Rx, midpoint_y])
        result.append([midpoint_x - Rx, midpoint_y])
        P1 = Rx * Rx - Ry * Ry * Rx + Ry * Ry / 4
        while Rx * Rx * y < Ry * Ry * x:
            if P1 < 0:
                P1 = P1 + 2 * Rx * Rx * y + 3 * Rx * Rx
                y += 1
                result.append([midpoint_x + x, midpoint_y + y])
                result.append([midpoint_x + x, midpoint_y - y])
                result.append([midpoint_x - x, midpoint_y + y])
                result.append([midpoint_x - x, midpoint_y - y])
            else:
                P1 = P1 + 2 * Rx * Rx * y - 2 * Ry * Ry * x + 2 * Ry * Ry + 3 * Rx * Rx
                y += 1
                x -= 1
                result.append([midpoint_x + x, midpoint_y + y])
                result.append([midpoint_x + x, midpoint_y - y])
                result.append([midpoint_x - x, midpoint_y + y])
                result.append([midpoint_x - x, midpoint_y - y])
        P2 = Rx * Rx * (y + 0.5)*(y + 0.5) + Ry * Ry * (x - 1) * (x - 1) - Rx * Rx * Ry * Ry
        while x > 0:
            if P2 <= 0:
                P2 = P2 + 2 * Rx * Rx * (y + 1) + Ry * Ry * (3 - 2 * x)
                x -= 1
                y += 1
                result.append([midpoint_x + x, midpoint_y + y])
                result.append([midpoint_x + x, midpoint_y - y])
                result.append([midpoint_x - x, midpoint_y + y])
                result.append([midpoint_x - x, midpoint_y - y])
            else:
                P2 = P2 + Ry * Ry * (3 - 2 * x)
                x -= 1
                result.append([midpoint_x + x, midpoint_y + y])
                result.append([midpoint_x + x, midpoint_y - y])
                result.append([midpoint_x - x, midpoint_y + y])
                result.append([midpoint_x - x, midpoint_y - y])
    
    return result


def draw_curve(p_list, algorithm):
    """绘制曲线

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 曲线的控制点坐标列表
    :param algorithm: (string) 绘制使用的算法，包括'Bezier'和'B-spline'（三次均匀B样条曲线，曲线不必经过首末控制点）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 绘制结果的像素点坐标列表
    """
    result = []
    if algorithm == 'Bezier':
        number = len(p_list)   #控制顶点数量
        nops = 500     #num_of_points
        for i in range(0, nops):
            point = deCasteljau(number - 1, 0, float(i / nops), p_list)
            point[0], point[1] = int(point[0]), int(point[1])
            result.append(point)
        '''    
        for i in range(len(p_list) - 1):  #控制多边形
            line = draw_line([p_list[i], p_list[i + 1]], 'DDA')
            result += line
        '''
    elif algorithm == 'B-spline': 
        n = len(p_list)
        nops = 500
        '''
        k = 4 #四阶
        u = k - 1 + (n - 2) / nops#[k - 1, n + 1]
        for i in range(1, nops):
            x = 0
            y = 0
            for j in range(0, n):
                B_ik = deBook_Cox(u, j, k)
                x += B_ik * p_list[j][0]
                y += B_ik * p_list[j][1]
                #print(int(x), int(y))
            #print(int(x), int(y))
            result.append([int(x), int(y)])
            u += (n - 2) / nops #n - k + 2
        '''
        for i in range(nops):
            for j in range(n - 3):  #n - k + 1(n+1个控制顶点，k，即3次)
                point = B_spline_matrix(i / nops, j, p_list)
                result.append(point)
        '''       
        for i in range(len(p_list) - 1):
            line = draw_line([p_list[i], p_list[i + 1]], 'DDA')
            result += line
        '''
    return result


def deCasteljau(r, i, u, p_list):
    if r == 0:
        return p_list[i]
    else:
        x = (1 - u) * deCasteljau(r - 1, i, u, p_list)[0] + u * deCasteljau(r - 1, i + 1, u, p_list)[0]
        y = (1 - u) * deCasteljau(r - 1, i, u, p_list)[1] + u * deCasteljau(r - 1, i + 1, u, p_list)[1]
        return [x, y]
'''
def deBook_Cox(u, i, k):  #B样条基函数
    if k == 1:
        if u >= i and u <= i + 1:
            return 1
        else:
            return 0
    else:
        mul_1 = 0
        mul_2 = 0
        if u - i != 0 or k - 1 != 0:
            mul_1 = (u - i) / (k - 1)
        if i + k - u != 0 or k - 1 != 0:
            mul_2 = (i + k - u) / (k - 1)
        return mul_1 * deBook_Cox(u, i, k - 1) + mul_2 * deBook_Cox(u, i + 1, k - 1)
'''
def B_spline_matrix(u, i, p_list):
    x = 1/6 * ((-u**3 + 3*u**2-3*u+1)*p_list[i][0] + (3*u**3-6*u**2+4)*p_list[i+1][0]+(-3*u**3+3*u**2+3*u+1)*p_list[i+2][0]+u**3*p_list[i+3][0])      
    y = 1/6 * ((-u**3 + 3*u**2-3*u+1)*p_list[i][1] + (3*u**3-6*u**2+4)*p_list[i+1][1]+(-3*u**3+3*u**2+3*u+1)*p_list[i+2][1]+u**3*p_list[i+3][1])
    return [int(x), int(y)]

      
def translate(p_list, dx, dy):
    """平移变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param dx: (int) 水平方向平移量
    :param dy: (int) 垂直方向平移量
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    result = p_list
    for i in range(len(result)):
        result[i][0] += dx
        result[i][1] += dy
    return result


def rotate(p_list, x, y, r):
    """旋转变换（除椭圆外）

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 旋转中心x坐标
    :param y: (int) 旋转中心y坐标
    :param r: (int) 顺时针旋转角度（°）
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    for i in range(len(p_list)):
        p_list[i][0] -= x
        p_list[i][1] -= y
        temp_x = p_list[i][0]
        temp_y = p_list[i][1]
        p_list[i][0] = int(temp_x * math.cos((360 - r) / 180 * math.pi) - temp_y * math.sin((360 - r) / 180 * math.pi))
        p_list[i][1] = int(temp_x * math.sin((360 - r) / 180 * math.pi) + temp_y * math.cos((360 - r) / 180 * math.pi))
        p_list[i][0] += x;
        p_list[i][1] += y
        
    return p_list


def scale(p_list, x, y, s):
    """缩放变换

    :param p_list: (list of list of int: [[x0, y0], [x1, y1], [x2, y2], ...]) 图元参数
    :param x: (int) 缩放中心x坐标
    :param y: (int) 缩放中心y坐标
    :param s: (float) 缩放倍数
    :return: (list of list of int: [[x_0, y_0], [x_1, y_1], [x_2, y_2], ...]) 变换后的图元参数
    """
    for i in range(len(p_list)):
        delta_x = (p_list[i][0] - x) * (s - 1)
        delta_y = (p_list[i][1] - y) * (s - 1)
        p_list[i][0] = int(p_list[i][0] + delta_x)
        p_list[i][1] = int(p_list[i][1] + delta_y)
    return p_list


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
    if x_min > x_min:
        x_min, x_max = x_max, x_min
    if y_min > y_max:
        y_min, y_max = y_max, y_min
    x0 = p_list[0][0]
    x1 = p_list[1][0]
    y0 = p_list[0][1]
    y1 = p_list[1][1]
    k = 0
    b = 0
    if x1 != x0:
        k = (y1 - y0) / (x1 - x0)
        b = y0 - k * x0
    if algorithm == 'Cohen-Sutherland':
        flag0 = compute_flag(x_min, y_min, x_max, y_max, x0, y0)
        flag1 = compute_flag(x_min, y_min, x_max, y_max, x1, y1)
        if k == 0:
            if x1 == x0:
                if x0 > x_max or x0 < x_min:
                    x0 = x1 = y0 = y1 = 0
                if (y0 < y_min and y1 < y_min) or (y0 > y_max and y1 > y_max):
                    x0 = x1 = y0 = y1 = 0
                else:
                    if y0 > y_max:
                        y0 = y_max
                    if y1 > y_max:
                        y1 = y_max
                    if y0 < y_min:
                        y0 = y_min
                    if y1 < y_min:
                        y1 = y_min
            else:  #y1 == y0
                if y0 > y_max or y0 < y_min:
                    x0 = x1 = y0 = y1 = 0
                if (x0 < x_min and x1 < x_min) or (x0 > x_max and x1 > x_max):
                    x0 = x1 = y0 = y1 = 0
                else:
                    if x0 > x_max:
                        x0 = x_max
                    if x1 > x_max:
                        x1 = x_max
                    if x0 < x_min:
                        x0 = x_min
                    if x1 < x_min:
                        x1 = x_min
        else:
            if (flag0 & flag1) != 0:
                x0 = x1 = y0 = y1 = 0
            else:
                if flag0 != 0 or flag1 != 0:  #顺序为上下右左
                    if (flag0 ^ flag1) & 8 == 8:
                        if flag0 & 8 == 8:  #0号在外
                            y0 = y_max
                            x0 = (y_max - b) / k
                            flag0 = compute_flag(x_min, y_min, x_max, y_max, x0, y0)
                        else:  #1号在外
                            y1 = y_max
                            x1 = (y_max - b) / k
                            flag1 = compute_flag(x_min, y_min, x_max, y_max, x1, y1)
                    if (flag0 ^ flag1) & 4 == 4:
                        if flag0 & 4 == 4:
                            y0 = y_min
                            x0 = (y_min - b) / k
                            flag0 = compute_flag(x_min, y_min, x_max, y_max, x0, y0)
                        else:  
                            y1 = y_min
                            x1 = (y_min - b) / k
                            flag1 = compute_flag(x_min, y_min, x_max, y_max, x1, y1)
                    if (flag0 ^ flag1) & 2 == 2:
                        if flag0 & 2 == 2:
                            x0 = x_max
                            y0 = k * x_max + b
                            flag0 = compute_flag(x_min, y_min, x_max, y_max, x0, y0)
                        else:  
                            x1 = x_max
                            y1 = k * x_max + b
                            flag1 = compute_flag(x_min, y_min, x_max, y_max, x1, y1)
                    if (flag0 ^ flag1) & 1 == 1:
                        if flag0 & 1 == 1:
                            x0 = x_min
                            y0 = k * x_min + b
                            flag0 = compute_flag(x_min, y_min, x_max, y_max, x0, y0)
                        else:  
                            x1 = x_min
                            y1 = k * x_min + b
                            flag1 = compute_flag(x_min, y_min, x_max, y_max, x1, y1)
        p_list[0][0] = int(x0)
        p_list[0][1] = int(y0)
        p_list[1][0] = int(x1)
        p_list[1][1] = int(y1)
    elif algorithm == 'Liang-Barsky':
        mu1 = 0.0
        mu2 = 1.0
        delta_x = x1 - x0
        delta_y = y1 - y0
        tx0 = tx1 = ty0 = ty1 = 0 #temp
        mu1, mu2, flag = update_mu(-delta_x, x0 - x_min, mu1, mu2)
        if flag == True:
            mu1, mu2, flag = update_mu(delta_x, x_max - x0, mu1, mu2)
            if flag == True:
                mu1, mu2, flag = update_mu(-delta_y, y0 - y_min, mu1, mu2)
                if flag == True:
                    mu1, mu2, flag = update_mu(delta_y, y_max - y0, mu1, mu2)
                    if flag == True:
                        if mu2 < 1:
                            x1 = x0 + mu2 * delta_x
                            y1 = y0 + mu2 * delta_y
                        if mu1 > 0:
                            x0 = x0 + mu1 * delta_x
                            y0 = y0 + mu1 * delta_y
                        tx0 = x0
                        ty0 = y0
                        tx1 = x1
                        ty1 = y1
        p_list[0][0] = int(tx0)
        p_list[0][1] = int(ty0)
        p_list[1][0] = int(tx1)
        p_list[1][1] = int(ty1)
    return p_list


def compute_flag(x_min, y_min, x_max, y_max, x, y):
    flag = 0
    if x < x_min:
        flag |= 1
    if x > x_max:
        flag |= 2
    if y < y_min:
        flag |= 4
    if y > y_max:
        flag |= 8
    return flag


def update_mu(p, q, mu1, mu2):
    r = 0
    if p != 0:
        r = q / p
    flag = True
    if p < 0:
        mu1 = max(mu1, r)
    elif p > 0:
        mu2 = min(mu2, r)
    elif p == 0:
        if q < 0:
            flag = False
    if mu1 > mu2:
        flag = False
    return mu1, mu2, flag

