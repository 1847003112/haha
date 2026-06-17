import json
from collections import defaultdict
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 作业要求：记账 Schema
EXPENSE_SCHEMA = {
    'type': 'object',
    'properties': {
        'amount': {'type': 'number', 'description': '金额 (元)'},
        'category': {
            'type': 'string',
            'enum': ['餐饮', '交通', '购物', '娱乐', '住房', '医疗', '其他']
        },
        'date': {'type': 'string', 'description': '日期 YYYY-MM-DD'},
        'note': {'type': 'string', 'description': '备注说明'},
        'type': {'type': 'string', 'enum': ['支出', '收入']}
    },
    'required': ['amount', 'category', 'type']
}

# 作业要求：月度汇总函数
def monthly_summary(records: list[dict]) -> dict:
    by_category = defaultdict(float)
    for r in records:
        if r.get('type') == '支出':
            by_category[r['category']] += r['amount']
    return {
        'total': sum(by_category.values()),
        'by_category': dict(by_category)
    }

# 记账对话主逻辑
class BillHelper:
    def __init__(self):
        self.records = []  # 存放所有账单记录
        self.system_prompt = f"""你是记账助手。
1. 用户描述消费内容，严格按照以下Schema提取信息，只输出JSON，不要额外文字
{json.dumps(EXPENSE_SCHEMA, ensure_ascii=False, indent=2)}
示例：用户输入"今天午餐花了38元"
输出：{{"amount":38,"category":"餐饮","type":"支出"}}

2. 当用户输入"本月消费汇总"，直接等待程序调用汇总函数输出结果。
"""

    def chat(self, user_text):
        # 调用大模型提取账单信息
        resp = client.chat.completions.create(
            model="qwen-turbo",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_text}
            ],
            response_format={"type": "json_object"}
        )
        content = resp.choices[0].message.content

        # 判断：查询汇总
        if user_text == "本月消费汇总":
            return monthly_summary(self.records)
        
        # 判断：新增账单
        try:
            bill = json.loads(content)
            self.records.append(bill)
            return bill
        except json.JSONDecodeError:
            return content

# 运行入口
if __name__ == "__main__":
    helper = BillHelper()
    print("记账助手已启动，输入内容记账，输入【本月消费汇总】查询统计，输入exit退出")
    while True:
        user_input = input("\n请输入：").strip()
        if user_input.lower() == "exit":
            break
        res = helper.chat(user_input)
        print(json.dumps(res, ensure_ascii=False, indent=2))