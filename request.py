import requests
import datetime
from pyquery import PyQuery as pq
import re

def request_english_day():
    requests.get('')
    

# 日历
def request_calender(data: str):
    
    params = {
        'date': data,
        'key': 'ebde19bd911cfdc29ba69075a955aed6'
    }
    
    # 发送GET请求
    response = requests.get('http://v.juhe.cn/calendar/day',params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('请求失败:', response.status_code)
        return None



# 天气
def request_weather():
    params = {
        'cityname': '武汉',
        'key': '6b1333527278ef25ef6b36e3755efe84'
    }
    response = requests.get('http://v.juhe.cn/weather/index', params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('请求失败:', response.status_code)
        return None
        
def request_time() -> datetime:
    response = requests.get('https://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp')
    if response.status_code == 200:
        data = response.json()
        time = int(data['data']['t']) / 1000
        return datetime.datetime.fromtimestamp(int(time))
    else:
        print('请求失败:', response.status_code)
        return datetime.datetime.now()



def request_weather2():
    host = 'https://weather.cma.cn'
    url = host + '/web/weather/56286.html'
    
    
    url2 = 'https://weather.cma.cn/api/now/56286'
    
    
    print('--->')
    response = requests.get(url)
    temps = []
    weather_imgs = []
    days_6 = []
    if response.status_code == 200:
        html = response.text
        doc = pq(html)
        try:
            temp = doc('.container .hp table.hour-table:eq(0) tbody tr:eq(2) td')
            for index,item in enumerate(temp):
                if index > 0:
                    temps.append(re.findall(r'\d+\.?\d*',pq(item).text())[0])
            
            
            weathers = doc('.container .hp .days>div')
            
            for index,item in enumerate(weathers):
                if index > 0:
                    path = pq(item)('img').attr('src')
                    t_high = pq(item)('.bardiv .high').text()
                    t_low = pq(item)('.bardiv .low').text()
                    val_high = re.findall(r'\d+\.?\d*',t_high)[0]
                    val_low = re.findall(r'\d+\.?\d*',t_low)[0]
                    days_6.append([val_high, val_low, host + path])
                    # temps.append(re.findall(r'\d+\.?\d*',pq(item).text())[0])
            print('over')
        except Exception as e:
            print('获取错误',e)
    else:
        print('请求失败:', response.status_code)
        
    return days_6

    
    # import urequests

    # url='http://i.tianqi.com/index.php?c=code&a=getcode&id=55&py=hongshan'

    # r = urequests.get(url)   # 发起HTTP的GET请求
    # content = r.text


    # import ure as re
    # print('农历')
    # nongli = re.search(r'<li class="t3">(.*?)</li>', content)
    # nongli = nongli.group(1)
    # print (nongli)

    # print('天气')
    # # r'<span style="font-size:14px;width: 70px;line-height: 18px;height: 18px;overflow: hidden;">雷阵雨</span>  这是是原文的串
    # tianqi = re.search(r'height: 18px;overflow: hidden;">(.*?)</span>', content)
    # tianqi = tianqi.group(1)
    # print (tianqi)

    # print('温度')
    # # r'<h5><span class="f1">27</span>~<span class="f2">34</span></h5>'  这是是原文的串
    # wendu = re.search(r'<h5><span class="f1">(.*?)</span>~<span class="f2">(.*?)</span></h5>', content)
    # wendua = wendu.group(1)
    # wendub = wendu.group(2)
    # print (wendua,wendub)

    # print('指数')
    # zhushui = re.search(r'height:36px"><h4>(.*?)</h4><p>(.*?)</p></a></div>', content)
    # zhushuia = zhushui.group(1)
    # zhushuib = zhushui.group(2)
    # print (zhushuia,zhushuib)
    
    