import requests
import re
from openai import OpenAI

# ================== 配置区 ==================
# 高德地图 API Key
GAODE_KEY = "aa21a4a012f9cbff3f759df62f48bfbe"

# 阿里云百炼（通义千问）配置
DASHSCOPE_API_KEY = "sk-aee853eb5fe34137b4800ef4561cdc15"
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL_NAME = "qwen-plus"

# 初始化通义千问客户端
client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url=DASHSCOPE_BASE_URL
)
# ===========================================

def get_weather(city):
    """获取城市实时天气，返回天气信息字典"""
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        "city": city.strip(),
        "key": GAODE_KEY,
        "extensions": "base",
        "output": "JSON"
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
        if data["status"] == "1" and data.get("lives"):
            live = data["lives"][0]
            weather_info = {
                "city": live["city"],
                "weather": live["weather"],
                "temperature": int(live["temperature"]),
                "humidity": int(live["humidity"]),
                "winddirection": live["winddirection"],
                "windpower": live["windpower"]
            }
            return weather_info
        else:
            print(" 获取天气失败，请检查城市名或网络")
            return None
    except Exception as e:
        print(f" 请求天气接口失败: {e}")
        return None

def get_clothing_advice_from_llm(city, weather_info):
    """调用通义千问大模型生成穿衣建议"""
    prompt = f"""你是一个生活助手，请根据以下{city}的天气信息，给出具体、实用、亲切的穿衣建议。要求：
- 建议包含衣物类型（如短袖、外套、羽绒服等）
- 如果下雨、下雪、大风等特殊天气，给出防护提示（雨具、防风等）
- 考虑温度和体感舒适度，可以提及材质或搭配
- 回答控制在30~80字，直接输出建议，不要有多余的解释

天气信息：
- 天气现象：{weather_info['weather']}
- 温度：{weather_info['temperature']}°C
- 湿度：{weather_info['humidity']}%
- 风力：{weather_info['windpower']}级，风向{weather_info['winddirection']}
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "你是一个生活助手，根据天气给出穿衣建议。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )
    advice = response.choices[0].message.content.strip()
    return advice

def main():
    city = input("请输入要查询的城市名（中文）：").strip()
    if not city or not re.search('[\u4e00-\u9fa5]', city):
        print(" 请输入正确的中文城市名")
        return

    # 1. 获取实时天气
    weather = get_weather(city)
    if not weather:
        return  # 天气获取失败直接结束，不输出任何建议

    # 打印天气信息
    print("\n===== 实时天气 =====")
    print(f"城市: {weather['city']}")
    print(f"天气: {weather['weather']}")
    print(f"温度: {weather['temperature']}°C")
    print(f"湿度: {weather['humidity']}%")
    print(f"风力: {weather['winddirection']} {weather['windpower']}级")

    # 2. 调用大模型生成穿衣建议（无兜底）
    print("\n===== 穿衣建议=====")
    try:
        advice = get_clothing_advice_from_llm(city, weather)
        print(advice)
    except Exception as e:
        print(f" 大模型生成建议失败: {e}")
        # 不输出任何兜底建议

if __name__ == "__main__":
    main()