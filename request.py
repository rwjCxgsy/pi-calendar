import requests
import datetime

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

