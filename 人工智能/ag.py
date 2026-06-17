from openai import OpenAI
from datetime import datetime
import json
import os
import random
import requests
from concurrent.futures import ThreadPoolExecutor
import time

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
    # 简易计算器工具
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
        res = eval(expr)
        return f"表达式 {expr} 的计算结果为：{res}"
    except Exception:
        return "计算失败，请输入合法的数学表达式（仅支持 + - * /）"

# 调用大模型
def get_response(messages):
    completion = client.chat.completions.create(
        model="qwen3.6-plus",
        extra_body={"enable_thinking": True},
        messages=messages,
        tools=tools,
        parallel_tool_calls=True
    )
    return completion

# 工具注册表
tool_registry = {
    "get_current_weather": get_current_weather,
    "get_current_time": get_current_time,
    "get_all_weather": get_all_weather,
    "calculator": calculator
}

def dispatch_tool(func_name, func_args):
    """通用工具分发器，自动匹配函数"""
    if func_name not in tool_registry:
        return f"❌ 不存在工具：{func_name}"
    return tool_registry[func_name](func_args)

# 线程池专用：单个工具执行包装函数
def run_single_tool(tool_call):
    """接收单个tool_call，执行工具并返回id+结果"""
    func_name = tool_call.function.name
    func_args = json.loads(tool_call.function.arguments)
    print(f"[并行线程] 调用工具 [{func_name}]，参数：{func_args}")
    res = dispatch_tool(func_name, func_args)
    return {
        "tool_call_id": tool_call.id,
        "content": res
    }

# ====================== 主逻辑 ======================
if __name__ == "__main__":
    print("输入 q 退出程序")
    while True:
        total_start = time.time()  # 单次对话计时起点
        user_input = input("请输入问题: ").strip()

        if user_input.lower() == 'q':
            print("再见！")
            break
        if not user_input:
            print("请输入有效的问题")
            continue

        # 每次对话重置上下文（如需多轮记忆，可把chat_messages移到循环外）
        messages = [{"role": "user", "content": user_input}]
        response = get_response(messages)
        assistant_output = response.choices[0].message
        if assistant_output.content is None:
            assistant_output.content = ""
        messages.append(assistant_output)

        # 无工具调用，直接输出
        if not assistant_output.tool_calls:
            print(f"无需调用工具，直接回复：{assistant_output.content}")
        else:
            print(f"\n模型一次性下发 {len(assistant_output.tool_calls)} 个工具任务，开启多线程并行执行...")
            tool_start = time.time()
            # 线程池并行执行工具
            with ThreadPoolExecutor(max_workers=10) as pool:
                all_tool_results = list(pool.map(run_single_tool, assistant_output.tool_calls))
            tool_cost = round(time.time() - tool_start, 3)

            # 追加工具返回结果到上下文
            for item in all_tool_results:
                messages.append({
                    "role": "tool",
                    "tool_call_id": item["tool_call_id"],
                    "content": item["content"]
                })

            # 大模型整合结果
            final_response = get_response(messages)
            final_ans = final_response.choices[0].message.content
            print("\n===== 助手最终整合回复 =====")
            print(final_ans)
            print(f"\n工具并行执行耗时：{tool_cost} 秒")

        # 单次对话总耗时
        total_cost = round(time.time() - total_start, 3)
        print(f"\n===================== 本次对话总耗时：{total_cost} 秒 =====================")