import requests
import re

# 高德地图API Key
KEY = "aa21a4a012f9cbff3f759df62f48bfbe"

def get_weather(city, option):
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    
    city = city.strip()
    
    # 空值检查
    if not city:
        print("X 请输入正确城市")
        return
    
    # 必须包含中文
    if not re.search('[\u4e00-\u9fa5]', city):
        print("X 请输入正确城市(必须是中文城市名)")
        return

    # ====================== 选项1：实时天气 ======================
    if option == '1':
        params_base = {
            "city": city,
            "key": KEY,
            "extensions": "base",
            "output": "JSON"
        }
        try:
            res_base = requests.get(url, params=params_base, timeout=10)
            data_base = res_base.json()
            
            if data_base["status"] == "1" and data_base.get("lives"):
                weather = data_base["lives"][0]
                print("===== 实时天气 =====")
                print(f"城市: {weather['city']}")
                print(f"天气: {weather['weather']}")
                print(f"温度: {weather['temperature']}°C")
                print(f"湿度: {weather['humidity']}%")
                print(f"风力: {weather['winddirection']} {weather['windpower']}级")
            else:
                print("X 获取天气信息失败")
        except Exception as e:
            print(f"X 请求失败: {e}")

    # ====================== 选项2：未来天气预报 ======================
    elif option == '2':
        params_all = {
            'city': city,
            'key': KEY,
            'extensions': 'all',
            'output': 'JSON'
        }
        try:
            res_all = requests.get(url, params=params_all, timeout=10)
            data_all = res_all.json()

            if data_all["status"] == "1" and data_all.get('forecasts'):
                forecasts = data_all['forecasts'][0]['casts']
                print("===== 未来4天天气预报 =====")
                
                for day in forecasts:
                    print(f"\n日期：{day['date']}")
                    print(f"白天天气：{day['dayweather']}")
                    print(f"夜间天气：{day['nightweather']}")
                    print(f"温度：{day['nighttemp']}°C ~ {day['daytemp']}°C")
                    print(f"风向：{day['daywind']} {day['daypower']}级")
            else:
                print("X 获取天气预报失败")
        except Exception as e:
            print(f"X 请求失败: {e}")

    # ====================== 无效选项 ======================
    else:
        print("X 无效选项")

# 测试
if __name__ == "__main__":
        opt = input("请选择功能：")
        if opt not in ["1","2"]:
            print("输入有误")
        city_name = input("请输入要查询的城市名：")
        get_weather(city_name, opt) 