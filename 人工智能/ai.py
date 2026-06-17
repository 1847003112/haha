from openai import OpenAI
from datetime import datetime, date
import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor
import time
from pydantic import BaseModel, Field, ValidationError
import pymysql
import re

# ===================== 数据库连接类 =====================
class DBHelper:
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host="localhost",
                user="root",
                password="123456",
                database="student_db",
                charset="utf8mb4"
            )
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            print("[OK] 数据库连接成功")
        except Exception as e:
            print("[ERROR] 数据库连接失败：", e)
            self.conn = None
            self.cursor = None

    def close(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()

db_helper = DBHelper()

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# ===================== Pydantic 参数模型 =====================
class WeatherLocationParams(BaseModel):
    location: str = Field(..., description="城市/县区名称，如：北京市、杭州市")

class CalculatorParams(BaseModel):
    expression: str = Field(..., description="数学表达式，支持 + - * / 及^，例如 1+2、sqrt(16),3^2")

class FileReadParams(BaseModel):
    file_path: str = Field(..., description="本地文件路径，仅允许读取当前项目目录及子目录文件")

class DateCalcParams(BaseModel):
    start_date: str = Field(..., description="起始日期，格式必须为 YYYY-MM-DD")
    days: int = Field(..., description="偏移天数，正数往后推，负数往前推")

class MysqlQueryParams(BaseModel):
    query_sql: str = Field(..., description="仅支持 SELECT 查询语句，禁止增删改操作")

class EmptyParams(BaseModel):
    pass

class DateBetweenParams(BaseModel):
    """两个日期之间的天数差"""
    start_date: str = Field(..., description="起始日期，格式 YYYY-MM-DD")
    end_date: str = Field(..., description="结束日期，格式 YYYY-MM-DD")

# ===================== 工具描述转换 =====================
def pydantic_to_tool_definition(model, name, desc):
    json_schema = model.model_json_schema()
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": desc,
            "parameters": json_schema
        }
    }

# ===================== 工具列表 =====================
tools = [
    pydantic_to_tool_definition(WeatherLocationParams, "get_current_weather", "查询指定城市实时天气"),
    pydantic_to_tool_definition(CalculatorParams, "calculator", "数学运算工具，支持加减乘除、开方"),
    pydantic_to_tool_definition(FileReadParams, "read_local_file", "读取本地文本文件"),
    pydantic_to_tool_definition(DateCalcParams, "date_calculate", "日期偏移计算（起始日期+偏移天数）"),
    pydantic_to_tool_definition(MysqlQueryParams, "mysql_select_query", "数据库SELECT查询"),
    pydantic_to_tool_definition(WeatherLocationParams, "get_all_weather", "查询指定城市未来天气预报"),
    pydantic_to_tool_definition(EmptyParams, "get_current_time", "获取当前日期和时间"),
    pydantic_to_tool_definition(DateBetweenParams, "days_between", "计算两个日期之间的天数差，例如：2023-07-14 到 2027-12-24 多少天；若计算到今日，可将结束日期设为今天"),
]

# ===================== 工具实现 =====================
def get_current_weather(arguments):
    KEY = "aa21a4a012f9cbff3f759df62f48bfbe"
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    location = arguments.get("location", "").strip()
    if len(location) < 2:
        return "参数错误：城市名称不合法"
    params = {"city": location, "key": KEY, "extensions": "base", "output": "JSON"}
    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
        if data.get("status") != "1":
            return f"天气查询失败：{data.get('info', '未知错误')}"
        w = data["lives"][0]
        return (f"城市: {w['city']}, 天气: {w['weather']}, 温度: {w['temperature']}°C, "
                f"湿度: {w['humidity']}%, 风力: {w['winddirection']} {w['windpower']}级")
    except Exception as e:
        return f"获取天气异常: {str(e)}"

def get_all_weather(arguments):
    KEY = "aa21a4a012f9cbff3f759df62f48bfbe"
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    location = arguments.get("location", "").strip()
    if len(location) < 2:
        return "参数错误：城市名称不合法"
    params = {"city": location, "key": KEY, "extensions": "all", "output": "JSON"}
    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
        if data.get("status") != "1":
            return f"天气预报查询失败：{data.get('info', '未知错误')}"
        forecasts = data['forecasts'][0]['casts']
        lines = [f"日期：{d['date']}, 白天：{d['dayweather']}, 夜间：{d['nightweather']}, "
                 f"温度：{d['nighttemp']}~{d['daytemp']}°C, 风向：{d['daywind']} {d['daypower']}级"
                 for d in forecasts]
        return "\n".join(lines)
    except Exception as e:
        return f"获取天气预报失败: {str(e)}"

def calculator(arguments):
    expr = arguments.get("expression", "").strip()
    allow_chars = set("0123456789+-*/.() sqrtpow23")
    if not all(c in allow_chars for c in expr):
        return "计算失败：表达式包含非法字符"
    try:
        safe = expr.replace("pow2", "**2").replace("pow3", "**3").replace("sqrt", "**0.5")
        res = eval(safe)
        return f"表达式 {expr} 计算结果：{res}"
    except Exception:
        return "计算失败，请输入合法数学表达式"

def read_local_file(arguments):
    target = arguments.get("file_path", "").strip()
    root = os.path.abspath(os.getcwd())
    abs_path = os.path.abspath(target)
    if not abs_path.startswith(root):
        return f"权限拒绝：禁止读取根目录外文件"
    if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
        return f"文件不存在或不是文件：{target}"
    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            content = f.read(2000)
        return f"文件内容：\n{content}"
    except Exception as e:
        return f"读取文件失败：{str(e)}"

def date_calculate(arguments):
    start = arguments.get("start_date", "").strip()
    days = arguments.get("days", 0)
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", start):
        return "日期格式错误，必须使用 YYYY-MM-DD"
    try:
        d = datetime.strptime(start, "%Y-%m-%d").date()
        target = date.fromordinal(d.toordinal() + days)
        return f"起始日期 {start} 偏移 {days} 天后：{target}"
    except Exception as e:
        return f"日期计算失败：{str(e)}"

def mysql_select_query(arguments):
    sql = arguments.get("query_sql", "").strip().upper()
    forbid = {"DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "TRUNCATE", "EXEC"}
    if not sql.startswith("SELECT"):
        return "禁止执行非SELECT查询"
    for kw in forbid:
        if kw in sql:
            return f"SQL拦截：检测到高危关键字 {kw}"
    if any(c in sql for c in ("'", ";", "--", "#")):
        return "SQL拦截：检测到疑似注入字符"
    if not db_helper.cursor:
        return "数据库未连接"
    try:
        db_helper.cursor.execute(sql)
        result = db_helper.cursor.fetchall()
        return f"查询结果共 {len(result)} 条：\n{json.dumps(result, ensure_ascii=False, indent=2)}"
    except Exception as e:
        return f"数据库查询失败：{str(e)}"

def get_current_time(arguments):
    now = datetime.now()
    week = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][now.weekday()]
    return f"当前时间：{now.strftime('%Y年%m月%d日 %H:%M:%S')}，{week}"

def days_between(arguments):
    start_raw = arguments.get("start_date", "").strip()
    end_raw = arguments.get("end_date", "").strip()
    start_clean = re.sub(r'[——\-]+', '-', start_raw)
    end_clean = re.sub(r'[——\-]+', '-', end_raw)
    pattern = r"^\d{4}-\d{1,2}-\d{1,2}$"
    if not re.match(pattern, start_clean) or not re.match(pattern, end_clean):
        return "日期格式错误，请使用 YYYY-MM-DD 格式，例如 2023-07-14"
    try:
        start = datetime.strptime(start_clean, "%Y-%m-%d").date()
        end = datetime.strptime(end_clean, "%Y-%m-%d").date()
        delta = (end - start).days
        return f"从 {start} 到 {end} 共 {delta} 天"
    except Exception as e:
        return f"日期计算失败：{str(e)}"

# ===================== 工具注册表 =====================
tool_registry = {
    "get_current_weather": (get_current_weather, WeatherLocationParams),
    "get_all_weather": (get_all_weather, WeatherLocationParams),
    "calculator": (calculator, CalculatorParams),
    "read_local_file": (read_local_file, FileReadParams),
    "date_calculate": (date_calculate, DateCalcParams),
    "mysql_select_query": (mysql_select_query, MysqlQueryParams),
    "get_current_time": (get_current_time, EmptyParams),
    "days_between": (days_between, DateBetweenParams),
}

# ===================== 分发和执行 =====================
def dispatch_tool(func_name, func_args):
    if func_name not in tool_registry:
        return f"❌ 不存在工具：{func_name}"
    tool_func, param_model = tool_registry[func_name]
    try:
        valid = param_model(**func_args)
        return tool_func(valid.model_dump())
    except ValidationError as e:
        return f"❌ 参数校验失败：{e}"

def run_single_tool(tool_call):
    func_name = tool_call.function.name
    func_args = json.loads(tool_call.function.arguments)
    print(f"[并行线程] 调用工具 [{func_name}]，参数：{func_args}")
    result = dispatch_tool(func_name, func_args)
    print(f"【工具原始结果】{result}")
    return {"tool_call_id": tool_call.id, "content": result}

def get_response(messages):
    return client.chat.completions.create(
        model="qwen3.6-plus",
        extra_body={"enable_thinking": True},
        messages=messages,
        tools=tools,
        parallel_tool_calls=True
    )

# ===================== 主循环 =====================
if __name__ == "__main__":
    print("===== 多工具智能调用系统 =====")
    while True:
        total_start = time.time()
        user_input = input("\n请输入问题(输入q退出)：").strip()
        if user_input.lower() == 'q':
            db_helper.close()
            print("再见！")
            break
        if not user_input:
            continue

        messages = [{"role": "user", "content": user_input}]
        response = get_response(messages)
        assistant = response.choices[0].message
        if assistant.content is None:
            assistant.content = ""
        messages.append(assistant)

        if not assistant.tool_calls:
            print(f"直接回复：{assistant.content}")
        else:
            print(f"\n开始并行执行 {len(assistant.tool_calls)} 个工具...")
            t_start = time.time()
            with ThreadPoolExecutor(max_workers=10) as pool:
                results = list(pool.map(run_single_tool, assistant.tool_calls))
            t_cost = round(time.time() - t_start, 3)

            for res in results:
                messages.append({"role": "tool", "tool_call_id": res["tool_call_id"], "content": res["content"]})

            final = get_response(messages)
            answer = final.choices[0].message.content
            print("\n===== 最终整合回复 =====")
            print(answer)
            print(f"工具并行耗时：{t_cost} 秒")

        print(f"本次对话总耗时：{round(time.time() - total_start, 3)} 秒")