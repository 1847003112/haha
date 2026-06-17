import json
import re
import os
from openai import OpenAI
from jsonschema import validate, ValidationError

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
class RoleManager:
    """多角色管理器"""

    def __init__(self, model: str = "qwen-turbo"):
        self.model = model
        self.roles: dict[str, dict] = {}        # 角色库
        self.role_histories: dict[str, list] = {}  # 各角色独立历史
        self.current_role: str | None = None    # 当前角色

    def register_role(self, role_id: str, name: str, system_prompt: str, description: str = ""):
        """注册一个角色"""
        self.roles[role_id] = {
            "name":          name,
            "system_prompt": system_prompt,
            "description":   description
        }
        self.role_histories[role_id] = []
        print(f"角色 [{name}] 注册成功 (id: {role_id})")

    def switch_role(self, role_id: str, keep_history: bool = False):
        """切换当前角色"""
        if role_id not in self.roles:
            raise ValueError(f"角色 {role_id} 不存在")

        old_role = self.current_role
        self.current_role = role_id

        if not keep_history:
            # 切换时可选择是否清空该角色的历史
            pass

        role_name = self.roles[role_id]["name"]
        print(f"角色切换：{self.roles[old_role]['name'] if old_role else '无'} → {role_name}")

    def chat(self, user_input: str) -> str:
        """用当前角色对话"""
        if self.current_role is None:
            raise RuntimeError("未设置当前角色，请先调用 switch_role()")

        role = self.roles[self.current_role]
        history = self.role_histories[self.current_role]

        history.append({"role": "user", "content": user_input})

        messages = [{"role": "system", "content": role["system_prompt"]}] + history

        response = client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})
        return reply

    def auto_route(self, user_input: str) -> str:
        """自动路由：让 AI 判断该用哪个角色，然后切换并回答"""
        role_descriptions = "\n".join(
            f"- {rid}: {info['name']} - {info['description']}"
            for rid, info in self.roles.items()
        )

        routing_prompt = f"""根据用户输入，选择最合适的角色ID来回答。
只输出角色ID，不要任何其他内容。

可用角色：
{role_descriptions}

用户输入：{user_input}
"""
        routing_response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": routing_prompt}]
        )
        role_id = routing_response.choices[0].message.content.strip()

        # 容错：如果返回的不是有效 role_id，用第一个角色
        if role_id not in self.roles:
            role_id = list(self.roles.keys())[0]

        self.switch_role(role_id)
        return self.chat(user_input)

    def list_roles(self):
        """显示所有角色"""
        print("\n=== 已注册角色 ===")
        for rid, info in self.roles.items():
            marker = " ← 当前" if rid == self.current_role else ""
            print(f"  [{rid}] {info['name']}: {info['description']}{marker}")


# 构建一个客服系统
manager = RoleManager()

manager.register_role(
    "1",
    "konwledge_teacher",
    "你是一名知识渊博的且有耐心的老师",
    "详细解释概念,询问概念"
)

manager.register_role(
    "2",
    "quiz_master",
    "你是一名专业的会根据知识点出问题的出题人",
    "出判断题或选择题进行考察学生对知识点的理解"
)

manager.register_role(
    "3",
    "studey_planner",
    "你是一名细心计划制定者",
    "制定学习计划和发现安排"
)

manager.list_roles()
# 手动切换角色 + 对话 
print("\n--- 手动切换角色对话 ---")
manager.switch_role("1")
print(manager.chat("什么是Python装饰器？"))

manager.switch_role("2")
print(manager.chat("出3道装饰器判断题"))

manager.switch_role("3")
print(manager.chat("制定7天装饰器学习计划"))
# # 自动路由测试
# test_inputs = [
#     "学习装饰器的概念",
#     "出3道装饰器的测试题",
#     "制"
# ]

# for user_input in test_inputs:
#     print(f"\n用户：{user_input}")
#     reply = manager.auto_route(user_input)
#     print(f"AI [{manager.roles[manager.current_role]['name']}]：{reply[:100]}...")