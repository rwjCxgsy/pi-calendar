import cv2
from typing import List
import numpy as np
from datetime import datetime




def draw_line(cv: cv2, image, y = 60):
    cv.line(image, (20, y), (280, y), (128, 128, 128), 1)

# 绘制顶部星期
def draw_date (cv: cv2, image):
    # 获取当前日期和时间
    now = datetime.now()

    # 获取年份
    year = now.year

    # 获取月份
    month = now.month

    # 获取日期
    day = now.day

    ((text_width, text_height), __base) = cv2.getTextSize('2', cv2.FONT_HERSHEY_DUPLEX, 0.5, 1)

    cv.putText(image, str(year) + '/' + str(month) + '/' + str(day), (20, 30 + text_height), cv2.FONT_HERSHEY_DUPLEX, 0.5, color=(0, 0, 0), thickness=1)





# 绘制当前为日期
def draw_day (cv: cv2, image):
    day = 25
    thickness = 4
    font_scale = 4
    ((text_width, text_height), __base) = cv2.getTextSize(str(day), cv2.FONT_HERSHEY_DUPLEX, fontScale=font_scale, thickness=thickness)
    cv.putText(image, str(day), (20 + int(260 / 2) - int(text_width / 2) , 110 + text_height), cv2.FONT_HERSHEY_DUPLEX, font_scale, color=(0, 0, 0), thickness=thickness)

# 绘制当月已过多久

def draw_progress (cv: cv2, image):
    day = 31
    total = 30
    thickness = 1
    font_scale = 0.4
    ((text_width, text_height), __base) = cv2.getTextSize(str(day) + ' / ' + str(total), cv2.FONT_HERSHEY_DUPLEX, fontScale=font_scale, thickness=thickness)
    cv.putText(image, str(day) + ' / ' + str(total), (20, 230 + text_height), cv2.FONT_HERSHEY_DUPLEX, font_scale, color=(0, 0, 0), thickness=thickness)

    gap_width = 3
    gap_height = 18
    for index in range(0, day):
        cv.line(image, (20 + 7 * index, 260), (20 + 7 * index, 260 + gap_height), (32, 32, 32), 2)

def draw_week (cv: cv2, image):
    week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    thickness = 1
    font_scale = 0.4
    ((text_width, text_height), __base) = cv2.getTextSize(week[1], cv2.FONT_HERSHEY_DUPLEX, fontScale=font_scale, thickness=thickness)
    cv.putText(image, week[1], (300 - 20 - text_width, 230 + text_height), cv2.FONT_HERSHEY_DUPLEX, font_scale, color=(0, 0, 0), thickness=thickness)


# 绘制湿度 温度 等



def draw(cv: cv2, image):
    draw_date(cv, image)
    draw_line(cv, image)
    draw_day(cv, image)
    draw_progress(cv, image)
    draw_line(cv, image, 250)
    draw_week(cv, image)



