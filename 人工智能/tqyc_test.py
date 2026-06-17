import requests
import re

KEY = "aa21a4a012f9cbff3f759df62f48bfbe"

def get_weather(city, option):
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    
    city = city.strip()
    
    if not city:
        print("X 请输入正确城市")
        return
    
    if not re.search('[\u4e00-\u9fa5]', city):
        print("X 请输入正确城市(必须是中文城市名)")
        return

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
                print(f"API返回: {data_base}")
        except Exception as e:
            print(f"X 请求失败: {e}")

if __name__ == "__main__":
    get_weather("北京", "1")
