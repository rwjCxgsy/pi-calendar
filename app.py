#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
# picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
# libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
# if os.path.exists(libdir):
#     sys.path.append(libdir)

import logging
# from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

width = 800
height = 480

# logging.basicConfig(level=logging.DEBUG)


def draw_dash_line(draw: ImageDraw.ImageDraw, x:int, y: int, length: int, gap = 2, color=1):
    for index in range(0, length):
        if index % 2 == 0:
            continue
        draw.point((x + index, y), fill=color)


def draw_line(draw: ImageDraw.ImageDraw, x:int, y: int, length: int, color=1, width = 1):
    draw.line((x, y, x + length, y), fill=color, width=width)


def draw_progress(draw: ImageDraw.ImageDraw, x:int, y: int, current: int, total: int, height: int, color=1):
    gsp = 6
    offset_x = 3
    # x += offset_x
    for index in range(0, total):
        if index < current:
            draw.rectangle((x + index * gsp, y, x + index * gsp + 2, y + height), fill=1)
        else:
            for k in range(0, height + 1):
                print(k)
                # draw.line((x + index * 4, y, x + index * 4, y + height), fill=2, width=2)
                if k % 2 == 0 or k == (height):
                    draw.point((x + index * gsp, y + k), fill=color)
                    # draw.point((x + index * gsp + 1, y + k), fill=color)
                    draw.point((x + index * gsp + 2, y + k), fill=color)


def draw_text(draw: ImageDraw.ImageDraw, text: str, x:int, y: int, font: ImageFont, width: int,  height: int, align: str, color = 1, base = 'none'):
    (sx, sy, ex, ey) = draw.textbbox((x, y), '2023/09/26', font=font)
    text_width = ex - sx
    text_height = ey - sy
    offset_x =  0 if align == 'left' else (width) / 2 if align == 'center' else width
    offset_y = int((height) / 2 - text_height / 2)
    print((x + offset_x, y + offset_y))
    draw.text((x + offset_x, y + offset_y), text, fill=color, font=font, align=align)

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

    draw.rectangle((0, 0, 300, 480), 0)

    draw_text(draw, '2023/9/26', 20, 20, font=font14, width=260, height=40, align='left', color=255)
    draw_dash_line(draw, 20,60, 260, 255)


    draw_text(draw, '22:26', 20, 21, font=font96, width=260, height=200, align='left', color=255)

    draw_text(draw, '27/30', 20, 221 - 30, font=font14, width=260, height=30, align='left', color=255)
    draw_text(draw, 'Tuesday', 20, 221 - 30, font=font14, width=260, height=30, align='right', color=255)
    draw_dash_line(draw, 20,221, 260, 255)

    draw_progress(draw, 20, 230, 27, 30, 12)


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
