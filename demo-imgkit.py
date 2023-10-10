from io import BytesIO
import io
import logging
# from tkinter import Image
import imgkit
from datetime import datetime 
import time
import requests
from tempita import Template
from PIL import Image,ImageDraw,ImageFont

from request import request_calender, request_time, request_weather2

weathers = []


with open('calender.tmpl', 'r') as file:
    template_content = file.read()


template = Template(template_content)

print('frame')
logging.info("epd7in5_V2 Demo")
# epd = epd7in5_V2.EPD()

logging.info("init and Clear")
# epd.init()
# epd.Clear()

width = 800
height = 480

Himage = Image.new('1', (width, height), 1)  # 255: clear the frame

start_time = time.time()





# Drawing on the Horizontal image
# logging.info("1.Drawing on the Horizontal image...")

date_info = request_time()

print('--->')
today_date = str(date_info.year) + '-' + str(date_info.month) + '-' + str(date_info.day)
current_time = str( date_info.hour) + ':' + str(date_info.minute)
# 时间
month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
per = str(date_info.day) + '/' + str(month_days[date_info.month])
weeks = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
print('--22->')
weather = request_calender(today_date)

# 定义曲线的控制点

days_6 = request_weather2()

progress = []
for item in range(1, month_days[date_info.month]):
    if item <= date_info.day:
        progress.append(1)
    else:
        progress.append(0) 

data = {
    'year_month': today_date,
    "week": str(weeks[date_info.weekday()]),
    "current_time": current_time,
    "total_day": str(month_days[date_info.month]),
    "day": date_info.day,
    "china_year": '拜月',
    "luck": '万事大吉',
    "progress": progress,
    "days_6": days_6
}

print(data)

rendered = template.substitute(data)


date = time.time()
options = {
    'format': 'jpg',
    "width": 800,
    "height": 480,
}
image_bytes = imgkit.from_string(rendered, False, options=options)

image_io = io.BytesIO(image_bytes)

# 使用 PIL 打开字节流中的图像
image = Image.open(image_io)
image = image.convert("1")
# image.show()
print(time.time() - date)