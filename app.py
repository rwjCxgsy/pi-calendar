#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import math
import numpy as np
# picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
# libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
# if os.path.exists(libdir):
#     sys.path.append(libdir)

import logging
# from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import re
from shapely.geometry import LineString
width = 800
height = 480

global_x = 0
global_y = 0



def translate(x: int, y: int):
    global global_x
    global_x = x
    global global_y
    global_y = y
    
def smoothstep(x):
    if x <= 0:
        return 0
    elif x >= 1:
        return 1
    else:
        return x * x * (3 - 2 * x)
    
def make_bezier(xys):
    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = pascal_row(n-1)
    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1-t)**i for i in range(n)])
            coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(
                tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result
    return bezier

def pascal_row(n, memo={}):
    # This returns the nth row of Pascal's Triangle
    if n in memo:
        return memo[n]
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n//2+1):
        # print(numerator,denominator,x)
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n&1 == 0:
        # n is even
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result))
    memo[n] = result
    return result
    
def is_point_inside_rectangle(point, rectangle):
    x, y = point  # 点的坐标
    x1, y1, x2, y2 = rectangle  # 矩形的边界

    if x1 <= x <= x2 and y1 <= y <= y2:
        return True
    else:
        return False
        
# logging.basicConfig(level=logging.DEBUG)


def draw_dash_line(draw: ImageDraw.ImageDraw, x:int, y: int, length: int, gap = 2, color=1):
    for index in range(0, length):
        if index % 2 == 0:
            continue
        draw.point((global_x + x + index, global_y + y), fill=color)


def draw_line(draw: ImageDraw.ImageDraw, x:int, y: int, length: int, color=1, width = 1):
    draw.line((global_x + x, global_y + y, global_x + x + length, global_y + y), fill=color, width=width)
    

def v2_length(s: (int, int), e: (int, int)):
    return int(math.sqrt((e[0] - s[0]) ** 2 + (e[1] - s[1]) ** 2))

def draw_rect(draw: ImageDraw.ImageDraw, x:int, y: int, width: int, height, color = 1, radius = 0):
    lt = (radius, radius)
    rt = (width - radius, radius)
    lb = (radius, height - radius)
    rb = (width - radius, height - radius)
    
    rect1 = (0, 0, radius, radius)
    rect2 = (width -radius, 0, width, radius)
    rect3 = (0, height - radius, radius, height)
    rect4 = (width -radius, height - radius, width, height)
    
    
    for offset_y in range(0, height):
        for offset_x in range(0, width):
            point = (offset_x, offset_y)
            if not radius != 0 and is_point_inside_rectangle(point, rect1) and v2_length(point, lt) >= radius:
                continue
            if not radius != 0 and is_point_inside_rectangle(point, rect2) and v2_length(point, rt) >= radius:
                continue
            if not radius != 0 and is_point_inside_rectangle(point, rect3) and v2_length(point, lb) >= radius:
                continue
            if not radius != 0 and is_point_inside_rectangle(point, rect4) and v2_length(point, rb) >= radius:
                continue
            if offset_y % 3 == 0  and offset_x % 3 == 0:
                draw.point((global_x + offset_x + x, global_y + offset_y + y), fill=color)


def draw_progress(draw: ImageDraw.ImageDraw, x:int, y: int, current: int, total: int, height: int, color=1):
    gsp = 6
    offset_x = 3
    # x += offset_x
    for index in range(0, total):
        if index < current:
            draw.rectangle((global_x + x + index * gsp, global_y + y, global_x + x + index * gsp + 2, global_y + y + height), fill=1)
        else:
            for k in range(0, height + 1):
                # draw.line((x + index * 4, y, x + index * 4, y + height), fill=2, width=2)
                if k % 2 == 0 or k == (height):
                    draw.point((global_x + x + index * gsp, global_y + y + k), fill=color)
                    # draw.point((global_x + x + index * gsp + 1, y + k), fill=color)
                    draw.point((global_x + x + index * gsp + 2, global_y + y + k), fill=color)


def draw_text(draw: ImageDraw.ImageDraw, text: str, x:int, y: int, font: ImageFont, width: int,  height: int, align: str, color = 1, base = 'none'):
    (sx, sy, ex, ey) = draw.textbbox((x, y), text, font=font)
    text_width = ex - sx
    text_height = ey - sy
    offset_x =  0 if align == 'left' else (width) / 2 if align == 'center' else width
    offset_y = int((height) / 2 - text_height / 2)
    anchor = 'lt'
    if align == 'center':
        anchor = 'mm'
    elif align == 'right':
        anchor = 'rt'
    draw.text((global_x + x + offset_x, global_y + y + offset_y ), text, fill=color, font=font, anchor=anchor)



def draw_text_multi(draw: ImageDraw.ImageDraw, text: str, x, y, width: int, max_height, font: ImageFont):
    width_limit = width
    # 计算每行文字的高度
    (sx, sy, ex, ey) = draw.textbbox((0, 0), "A", font=font)
    
    text_height = int(ey - sy)

    # 按限定宽度进行换行
    lines = []
    current_line = ''
    
    texts = re.split(r'\s', text)
    
    for word in texts:
        (tsx, tsy, tex, tey) = draw.textbbox((0, 0), current_line + ' ' + word, font=font)
        if (tex - tsx) <= width_limit:
            current_line += (' ' + word)
        else:
            for item in current_line.split('\n'):
                lines.append(item)
                current_line = word
    lines.append(current_line)
    
    # print(lines)
    
    current_height = 0
    for index, text in enumerate(lines):
        if current_height >= max_height:
            break
        # print((global_x +  x, global_y + y + index * 30))
        draw.text((global_x +  x, global_y + y + index * 30), text, fill=0, font=font)
        current_height = (index + 1) * 30;
    



try:
    logging.info("epd7in5_V2 Demo")
    # epd = epd7in5_V2.EPD()
    
    logging.info("init and Clear")
    # epd.init()
    # epd.Clear()

    font_c_14 = ImageFont.truetype(os.path.join('./AaGuDianKeBenSong-2.ttf'), 14)
    font_c_16 = ImageFont.truetype(os.path.join('./AaGuDianKeBenSong-2.ttf'), 14)

    font96 = ImageFont.truetype(os.path.join('UNSII-2.ttf'), 96)
    font18 = ImageFont.truetype(os.path.join('UNSII-2.ttf'), 18)
    font14 = ImageFont.truetype(os.path.join('UNSII-2.ttf'), 14)

    # Drawing on the Horizontal image
    # logging.info("1.Drawing on the Horizontal image...")
    Himage = Image.new('1', (width, height), 255)  # 255: clear the frame

    draw = ImageDraw.Draw(Himage)

    # 背景 
    draw.rectangle((0, 0, 300, 480), 0)
    translate(20, 20)

    # 日期
    draw_text(draw, '2023/9/26', 0, 6, font=font14, width=260, height=40, align='left', color=255)
    # 分割线
    draw_dash_line(draw, 0,40, 260, 255)

    # 时间
    draw_text(draw, '22:26', 0, 41, font=font96, width=260, height=200, align='center', color=255)

    # 进度
    draw_text(draw, '27/30', 0, 221 - 30, font=font14, width=260, height=30, align='left', color=255)
    # 星期
    draw_text(draw, 'Tuesday', 0, 221 - 30, font=font14, width=260, height=30, align='right', color=255)
    # 分割线
    draw_dash_line(draw, 0,221, 260, 255)
    # 进度条
    draw_progress(draw, 0, 230, 27, 30, 12)
   
    draw_text(draw,'温度：37°', 0, 250, font=font_c_14, width=260, height=20, align='left')
   
    draw_text(draw,'湿度：59%', 0, 270, font=font_c_14, width=260, height=20, align='left')
   
    text = u"""\甲午(马)年八月十八\n祭祀 出行 扫舍 馀事勿取\n诸事不宜"""
    
    # draw.multiline_text((0, 250), text, fill=1, font=font_c_14, spacing=6)
    draw_text(draw,'甲午(马)年八月十八', 0, 290, font=font_c_14, width=260, height=20, align='left')
    # draw_text(draw,'祭祀 出行 扫舍 馀事勿取', 0, 310, font=font_c_14, width=260, height=20, align='left')
    # draw_text(draw,'诸事不宜', 0, 330, font=font_c_14, width=260, height=20, align='left')
    
    translate(20, 360)
    # draw_rect(draw, 0, 360, 40, 40, color=0, radius=3)
    # 定义曲线的控制点
    


    path = [35, 28, 32, 36, 30]


    start_y = 420
    max_value = max(path)
    min_value = min(path)
    dt = int(max_value - min_value)
    
    max_height = 40
    
    step = int(260 / 4)

    for (index, item) in enumerate(range(1, len(path))):
        sy = path[item -1]
        ey = path[item]
        print(sy, ey)
        for k in range(0, step):
            draw.point((20 + int(index * step + k), int(start_y + (max_value - (sy + smoothstep(k/step) * (ey - sy))) * (max_height / dt))), fill=1)

    # 绘制曲线
    # draw.line(points, fill='blue', width=2, joint='curve')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # 右侧内容
    translate(305, 0)
    draw_rect(draw, 0, 0, width-305, height=50, color=0)
    # 绘制标题
    draw_text(draw, 'A puma at large', 0, 0, font18, 480, 50, 'center', color=0)
    translate(320, 50)
    
    content = u'''We were using this to help teams optimise their players and know how to manage them for their games. We called this solution Performetric. It is a non-invasive programme that runs on PCs to analyse mental fatigue and stress based on how players click their mice and keyboards.
So, in our early days, that was in 2018, we were serving eSports teams to help them monitor their players' stress and anxiety levels so they could know what to do. While doing that, we were also looking for other ways to expand our reach.
Eventually, as we analysed player behaviours and their use of their hardware, we started the solution that is now known as Anybrain’s AI Anti-Cheat. We spent the earlier years testing the products and then pitching prospects to show them how our solution works and why we are better than other existing ones in the market. We were trying to gain recognition for what we were doing. Seeking that recognition took a while, but it has brought us here eight years later.
Anh-Vu: So, yes, we have existed as a team for a long time. But I joined them more recently. André and Serafim began working on the technology for our line of products many years ago.'''
    
    draw_text_multi(draw, content, 0, 0, 460, max_height = 410, font=font14)
    
    # 绘制内容
    
    Himage.show()


    # draw.text((10, 20), '7.5inch e-Paper', font=font14, fill = 0)
    # draw.text((150, 0), u'微雪电子', font=font14, fill = 0)
    # draw.line((20, 50, 70, 100), fill = 0)
    # draw.line((70, 50, 20, 100), fill = 0)
    # draw.rectangle((20, 50, 70, 100), outline = 0)
    # draw.line((165, 50, 165, 100), fill = 0)
    # draw.line((140, 75, 190, 75), fill = 0)
    # draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
    # draw.rectangle((80, 50, 130, 100), fill = 0)
    # draw.chord((200, 50, 250, 100), 0, 360, fill = 0)
    Himage.save('image2.jpg')
    # epd.display(epd.getbuffer(Himage))
    # time.sleep(2)

    # Drawing on the Vertical image
    # logging.info("2.Drawing on the Vertical image...")
    # Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    # draw = ImageDraw.Draw(Limage)
    # draw.text((2, 0), 'hello world', fill = 0)
    # draw.text((2, 20), '7.5inch epd', fill = 0)
    # draw.text((20, 50), u'微雪电子', fill = 0)
    # draw.line((10, 90, 60, 140), fill = 0)
    # draw.line((60, 90, 10, 140), fill = 0)
    # draw.rectangle((10, 90, 60, 140), outline = 0)
    # draw.line((95, 90, 95, 140), fill = 0)
    # draw.line((70, 115, 120, 115), fill = 0)
    # draw.arc((70, 90, 120, 140), 0, 360, fill = 0)
    # draw.rectangle((10, 150, 60, 200), fill = 0)
    # draw.chord((70, 150, 120, 200), 0, 360, fill = 0)
    # epd.display(epd.getbuffer(Limage))
    # time.sleep(2)

    # logging.info("3.read bmp file")
    # Himage = Image.open(os.path.join(picdir, '7in5_V2.bmp'))
    # epd.display(epd.getbuffer(Himage))
    # time.sleep(2)

    # logging.info("4.read bmp file on window")
    # Himage2 = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    # bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
    # Himage2.paste(bmp, (50,10))
    # epd.display(epd.getbuffer(Himage2))
    # time.sleep(2)

    # logging.info("Clear...")
    # epd.init()
    # epd.Clear()

    # logging.info("Goto Sleep...")
    # epd.sleep()
    
except IOError as e:
    # logging.info(e)
    print(e)
    
except KeyboardInterrupt:    
    # logging.info("ctrl + c:")
    # epd7in5_V2.epdconfig.module_exit()
    exit()
