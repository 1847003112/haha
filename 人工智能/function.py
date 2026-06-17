from openai import OpenAI
from datetime import datetime
import json
import os
import random
import requests
# 初始化客户端
client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 工具列表：新增计算器工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的实时天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_all_weather",
            "description": "当你想查询指定城市的未来多天天气预报时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当用户询问当前时间、日期、星期时使用该工具，无需传入参数。",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    # 新增：简易计算器工具
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "用于四则运算，计算加减乘除数学表达式，如 1+2、10*5、20/4、15-3",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "待计算的数学表达式"
                    }
                },
                "required": ["expression"],
            },
        },
    }
]

# 实时天气查询
def get_current_weather(arguments):
    KEY = "aa21a4a012f9cbff3f759df62f48bfbe"
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    location = arguments.get("location")
    params_base = {
        "city": location,
        "key": KEY,
        "extensions": "base",
        "output": "JSON"
    }
    try:
        res_base = requests.get(url, params=params_base, timeout=10)
        data_base = res_base.json()
        weather = data_base["lives"][0]
        result = f"城市: {weather['city']}, 天气: {weather['weather']}, 温度: {weather['temperature']}°C, 湿度: {weather['humidity']}%, 风力: {weather['winddirection']} {weather['windpower']}级"
        return result
    except Exception as e:
        print(f"X 请求失败: {e}")
        return f"获取天气失败: {str(e)}"

# 未来多天天气预报
def get_all_weather(arguments):
    KEY = "aa21a4a012f9cbff3f759df62f48bfbe"
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    location = arguments.get("location")
    params_all = {
        "city": location,
        "key": KEY,
        "extensions": "all",
        "output": "JSON"
    }
    try:
        res_all = requests.get(url, params=params_all, timeout=10)
        data_all = res_all.json()
        forecasts = data_all['forecasts'][0]['casts']
        result_lines = []
        for day in forecasts:
            day_info = f"日期：{day['date']}, 白天天气：{day['dayweather']}, 夜间天气：{day['nightweather']}, 温度：{day['nighttemp']}°C ~ {day['daytemp']}°C, 风向：{day['daywind']} {day['daypower']}级"
            result_lines.append(day_info)
        return "\n".join(result_lines)
    except Exception as e:
        print(f"X 请求失败: {e}")
        return f"获取天气预报失败: {str(e)}"

# 获取当前时间
def get_current_time(arguments):
    now = datetime.now()
    week_map = {0: "星期一", 1: "星期二", 2: "星期三", 3: "星期四", 4: "星期五", 5: "星期六", 6: "星期日"}
    week = week_map[now.weekday()]
    time_str = now.strftime("%Y年%m月%d日 %H:%M:%S")
    return f"当前时间：{time_str}，{week}"

# 计算器工具函数
def calculator(arguments):
    expr = arguments.get("expression", "")
    try:
        # 执行四则运算
        res = eval(expr)
        return f"表达式 {expr} 的计算结果为：{res}"
    except:
        return "计算失败，请输入合法的数学表达式（仅支持 + - * /）"

# 调用大模型
def get_response(messages):
    completion = client.chat.completions.create(
        model="qwen3.6-plus",
        extra_body={"enable_thinking": False},
        messages=messages,
        tools=tools,
        parallel_tool_calls=True
    )
    return completion

# 主对话循环
print("===== 天气&时间&计算器助手 =====")
print("支持查询实时天气、未来天气预报、当前时间、数学四则运算")
print("输入'q'结束对话\n")
messages = [{"role": "system", "content": "你是全能助手，根据用户问题调用对应工具并整理结果回答"}]

while True:
    user_input = input("请输入问题: ").strip()

    if user_input.lower() in ['q']:
        print(" 再见！")
        break
    if not user_input:
        print(" 请输入有效的问题")
        continue

    messages.append({"role": "user", "content": user_input})
    response = get_response(messages)
    assistant_output = response.choices[0].message

    if assistant_output.content is None:
        assistant_output.content = ""
    messages.append(assistant_output)

    if assistant_output.tool_calls is None:
        print(f"\n助手回复：{assistant_output.content}\n")
    else:
        while assistant_output.tool_calls is not None:
            for tool_call in assistant_output.tool_calls:
                tool_call_id = tool_call.id
                func_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                print(f"正在调用工具 [{func_name}]，参数：{arguments}")

                # 工具路由分发
                if func_name == "get_current_weather":
                    tool_result = get_current_weather(arguments)
                elif func_name == "get_all_weather":
                    tool_result = get_all_weather(arguments)
                elif func_name == "get_current_time":
                    tool_result = get_current_time(arguments)
                elif func_name == "calculator":
                    tool_result = calculator(arguments)
                else:
                    tool_result = f"未知的工具: {func_name}"

                tool_message = {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": tool_result,
                }
                messages.append(tool_message)

            # 二次调用模型生成最终回答
            response = get_response(messages)
            assistant_output = response.choices[0].message
            if assistant_output.content is None:
                assistant_output.content = ""
            messages.append(assistant_output)
        print(f"\n助手回复:{assistant_output.content}\n")