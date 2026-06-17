import json
import re
import os
from openai import OpenAI
from jsonschema import validate, ValidationError

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# def safe_parse_json(text: str) -> dict | None:
#     """安全解析 AI 返回的 JSON 字符串，多层兜底容错"""

#     # 1. 直接解析纯 JSON
#     try:
#         return json.loads(text)
#     except json.JSONDecodeError:
#         pass

#     # 2. 提取 markdown json代码块
#     pattern_code = r'```(?:json)?\s*([\s\S]+?)```'
#     match = re.search(pattern_code, text)
#     if match:
#         try:
#             return json.loads(match.group(1))
#         except json.JSONDecodeError:
#             pass

#     # 3. 提取全文第一个 {} JSON对象
#     pattern_obj = r'\{[\s\S]+?\}'
#     match = re.search(pattern_obj, text)
#     if match:
#         try:
#             return json.loads(match.group(0))
#         except json.JSONDecodeError:
#             pass

#     # 全部策略失效
#     return None
# system_prompt = """
# 你是一个信息提取助手。
# 每次收到用户输入时,你都要输出标准JSON格式的提取结果。
# 不要提取size
# 示例
# 输入：红色T恤，小码，售价89元，库存200件
# 输出：{'color': '红色', 'type': 'T恤', 'price': '89元', 'stock': '200件'}
# """

# user_input = "1.红色T恤，小码，售价89元，库存200件.2.蓝色牛仔裤，M码，售价179元，库存50件.3.白色运动鞋，43码，售价299元，库存30件，"

# # 调用大模型
# response = client.chat.completions.create(
#     model="qwen-plus",
#     messages=[
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": user_input}  
#     ],
#     response_format={"type": "json_object"} 
# )
# # 解析并打印结果
# result = response.choices[0].message.content
# print(json.loads(result))
#------------------------------------------------
# comment_schema = {
#     "type": "object",
#     "properties": {
#         "comment_id": {
#             "type": "string",
#             "description": "评论唯一编号，如 COM-20240101-001"
#         },
#         "content": {
#             "type": "string",
#             "description": "用户原始评论内容"
#         },
#         "sentiment": {
#             "type": "string",
#             "enum": ["正面", "负面", "中性"],
#             "description": "评论情感倾向"
#         },
#         "score": {
#             "type": "number",
#             "description": "评分分数，范围 0-5"
#         },
#         "tags": {
#             "type": "array",
#             "description": "评论标签/关键词列表",
#             "items": {
#                 "type": "string"
#             }
#         },
#         "need_review": {
#             "type": "boolean",
#             "description": "是否需要人工回复,规则:评分小于3则标记为需要回复"
#         }
#     },
#     "required": ["comment_id", "content", "sentiment", "score", "tags", "need_review"]
# }
# def extract_with_schema(text: str, schema: dict, model: str = "qwen-plus") -> dict:
#     """用 Schema 约束提取结构化信息"""

#     comment_schema = json.dumps(schema, ensure_ascii=False, indent=2)

#     prompt = f"""请从以下文本中提取信息，严格按照 JSON Schema 输出，只输出 JSON 不加任何说明：

# JSON Schema：
# {comment_schema}

# 待提取文本：
# {text}

# 注意：
# 1. 只输出符合 Schema 的 JSON
# 2. required 字段必须存在
# 3. enum 字段只能使用给定的值"""

#     response = client.chat.completions.create(
#         model=model,
#         messages=[{"role": "user", "content": prompt}],
#         response_format={"type": "json_object"}
#     )
#     return json.loads(response.choices[0].message.content)
# structured_prompt = """
# <task>
#   <role>你是一位专业的代码审查工程师</role>
#   <input>
#     <code language="python">
#       def add(a, b):
#           return a - b   # 这里有 bug
#     </code>
#   </input>
#   <requirements>
#     <item>找出代码中的 bug</item>
#     <item>给出修复建议</item>
#     <item>评估代码质量（1-10分）</item>
#   </requirements>
#   <output_format>
#     以 JSON 格式返回：{"bug": "...", "fix": "...", "score": 数字}
#   </output_format>
# </task>
# """

# response = client.chat.completions.create(
#     model="qwen-turbo",
#     messages=[{"role": "user", "content": structured_prompt}],
#     response_format={"type": "json_object"}
# )
# print(json.loads(response.choices[0].message.content))
#------------------------------------------------------------------
# structured_prompt = """
# <task>
#   <role>专业英文新闻分析师，精准提取新闻关键信息</role>
#   <description>请仔细阅读下方英文新闻内容，严格按照要求提取信息并输出指定格式结果</description>
#   <input>
#     <news_content>
# Author: Tom Green
# Date: June 12, 2026
# With the arrival of warm summer days, outdoor activities have swept across the country. 
# Hiking, camping and cycling are the most popular choices for people to spend weekends and holidays. 
# Many families and young groups choose to get close to nature instead of staying indoors all day.
# Health experts say regular outdoor exercise helps strengthen bodies and relieve daily stress. 
# It also allows people to stay away from electronic devices and enjoy quality time with family and friends. 
# More people now realize the great benefits of outdoor life and plan more outdoor trips in the coming months.</news_content>
#   </input>
#   <requirements>
#     <item>提取新闻原始标题,如果没有标题自己总结一下,可以使用中文标题</item>
#     <item>提取新闻作者姓名</item>
#     <item>提取新闻发布时间</item>
#     <item>撰写简短中文摘要</item>
#     <item>提取核心关键词以列表形式呈现</item>
#   </requirements>
#   <output_format>
#     仅返回标准JSON字符串、markdown、多余文字字段,使用中文严禁使用其他语言如下:
#     {
#       "title": "新闻标题",
#       "author": "新闻作者",
#       "time": "发布时间",
#       "summary": "新闻摘要",
#       "keywords": ["关键词"]
#     }
#   </output_format>
# </task>
# """

# response = client.chat.completions.create(
#     model="qwen-turbo",
#     messages=[{"role": "user", "content": structured_prompt}],
#     response_format={"type": "json_object"}
# )
# print(json.loads(response.choices[0].message.content))
#----------------------------------------------------------------------------
class AIRole:
    """可持久化的 AI 角色"""

    def __init__(self, name: str, system_prompt: str, model: str = "qwen-turbo"):
        self.name = name
        self.system_prompt = system_prompt
        self.model = model
        self.history: list[dict] = []  # 对话历史

    def chat(self, user_input: str) -> str:
        """发送消息，保留上下文"""
        self.history.append({"role": "user", "content": user_input})

        messages = [{"role": "system", "content": self.system_prompt}] + self.history

        response = client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        reply = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def reset(self):
        """重置对话历史，保留角色设定"""
        self.history = []
        print(f"[{self.name}] 对话历史已清空")

    def get_history_count(self) -> int:
        return len(self.history) // 2  # 轮数


# 创建两个不同角色
python_tutor = AIRole(
    name="审查员",
    system_prompt="""你是一个严格代码审查官,发现bug态度严格,要求学员修改后才能通过
    1.语言简洁，通俗易懂
    2.每次回答的时候都用最直接的语言指出问题
    3.对代码讲解只回答有关python的问题
    4.输出格式
    解释部分:2-3句话
    代码示例:用python代码块包裹
    """
)

career_advisor = AIRole(
    name="伙伴",
    system_prompt="""你是一个温柔学习伙伴,鼓励式教学,即使代码错了也先肯定亮点
    1.回答的时候对我进行情绪安慰
    """
)

# 测试
print(python_tutor.chat("""
def add(a, b)
    return a + b
num1 = 10
num2 = "20"
result = add(num1, num2)
print("结果：", result)
对代码进行检查"""))
print('-----------------')
print(career_advisor.chat("""
def add(a, b)
    return a + b
num1 = 10
num2 = "20"
result = add(num1, num2)
print("结果：", result)
对代码进行检查             
"""))
# # 测试
# text = "这款手机屏幕很清晰,就是电池差"
# result = extract_with_schema(text, comment_schema)
# print(json.dumps(result, ensure_ascii=False, indent=2))
# def validate_ai_output(data: dict, schema: dict) -> tuple[bool, str]:
#     """校验 AI 输出是否符合 Schema"""
#     try:
#         validate(instance=data, schema=schema)
#         return True, "校验通过"
#     except ValidationError as e:
#         return False, f"校验失败：{e.message}"

# # 完整流程：提取 + 校验
# result = extract_with_schema(text, comment_schema)
# is_valid, msg = validate_ai_output(result, comment_schema)

# if is_valid:
#     print("提取成功！")
#     print(f"客户：{result['customer']}")
#     print(f"总金额：{result['total']}")
#     for item in result.get('items', []):
#         print(f"  - {item['product']} × {item['quantity']} = {item['price'] * item['quantity']}元")
# else:
#     print(f"数据不合规：{msg}")