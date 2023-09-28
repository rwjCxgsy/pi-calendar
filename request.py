import requests
import datetime

def request_english_day():
    requests.get('')
    

# 日历
def request_calender():
    
    params = {
        'date': '2023-9-28',
        'key': 'ebde19bd911cfdc29ba69075a955aed6'
    }
    
    # 发送GET请求
    response = requests.get('http://v.juhe.cn/calendar/day',params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print('请求失败:', response.status_code)



# 天气
def request_weather():
    params = {
        'cityname': 'CHXX0008',
        'key': '6b1333527278ef25ef6b36e3755efe84'
    }
    response = requests.get('http://v.juhe.cn/weather/index', params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print('请求失败:', response.status_code)
        
def request_time() -> datetime:
    response = requests.get('https://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp')
    if response.status_code == 200:
        data = response.json()
        time = int(data['data']['t']) / 1000
        return datetime.datetime.fromtimestamp(int(time))
    else:
        print('请求失败:', response.status_code)

request_weather()
request_calender()
print(request_time())