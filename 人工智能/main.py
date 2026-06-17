# import my_cale
# print(my_cale.add(3,5))
# print(my_cale.multiply(4,6))
# print(my_cale.PI)
# from my_cale import add
# print(add(3,5))
# import my_cale as f
# print(f.add(2,4))
#----------------------------------
# from datetime import datetime
# now=datetime.now()
# n=now.strftime('%Y-%m-%d %H:%M:%S')
# m=now.strftime('%A,%B %d,%Y')
# print(n)
# print(m)
#---------------------------------
#import mima
#n=mima.mi()
#print(n)
#-------------------
# import showtime
# n=showtime.show_time()
# print(n)
#---------------------
# import json
# user_data={'name':'李四','age':30,'skills':['python','java']}
# json_str=json.dumps(user_data,ensure_ascii=True,indent=4)
# print('转换后的JSON字符串:\n',json_str)
# parsed_dict=json.loads(json_str)
# print('\n提取名字;',parsed_dict['name'])
# print('提取技能列表：',parsed_dict['skills'])
#----------------------------------------------
# import json
# m={
# "company": "Alibaba",
# "employees": [{"name": "Alice", "position": "Engineer", "salary": 10000},
#               {"name": "Bob", "position": "Manager", "salary": 15000}],
# "location": "Hangzhou"}
# n=json.dumps(m,ensure_ascii=False,indent=3)
# a=json.loads(n)
# print('提取公司名字:',a['company'])
# print('所在地：',a['location'])
# b = a['employees']
# c = 0  
# for i in b:
#     name = i['name']
#     position = i['position']
#     salary = i['salary']
#     print(f"姓名：{name}，职位：{position}")
#     c += salary  
# avg_salary = c / len(b)
# print(f"员工平均工资：{avg_salary}")
#----------------------------------------------------------------------
# import requests
# response = requests.get('https://httpbin.org/get')
# print('状态码：', response.status_code)
# print('\n响应头：')
# print(response.headers)
# print('\n响应内容：')
# print(response.text)
# -----------------------------------------------
# import requests
# resp = requests.get('https://httpbin.org/status/404')
# print("状态码：", resp.status_code)
# try:
#     resp.raise_for_status()
# except requests.HTTPError as e:
#     print("请求出错：", e)
#---------------------------------------------------
# import requests
# try:
#     r=requests.get('https://httpbin.org/delay/2',timeout=1)
#     r.raise_for_status()
#     print("请求成功")
# except requests.exceptions.Timeout:
#     print('超时')
# ------------------------------------
import requests
try:
    response = requests.get('http://httpbin.org/ip')
    response.raise_for_status()
    response_data = response.json()
    public_ip = response_data.get("origin")
    print(f" 你的公网IP地址为:{public_ip}")

except requests.exceptions.ConnectionError:
    print(" 错误：网络连接失败，请检查你的网络状态")
except requests.exceptions.Timeout:
    print(" 错误：请求超时，请稍后重试")
except requests.exceptions.HTTPError as e:
    print(f" HTTP请求错误,状态码:{e.response.status_code}")
except Exception as e:
    print(f" 未知错误：{str(e)}")
