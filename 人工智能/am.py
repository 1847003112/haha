import json
import os
from openai import OpenAI
from datetime import datetime

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# ── 角色定义 ──────────────────────────────
ROLES = {
    "qa": {
        "name": "知识助手",
        "prompt": """你是一个知识渊博的问答助手。
回答问题时，输出 JSON 格式：
{"answer": "回答内容", "confidence": "高/中/低", "related_topics": ["相关话题1", "相关话题2"]}""",
        "output": "json"
    },
    "task": {
        "name": "任务管家",
        "prompt": """你是一个任务管理助手。
当用户描述任务时，提取任务信息输出 JSON：
{"task_name": "任务名", "deadline": "截止日期或null", "priority": "高/中/低", "tags": ["标签"]}
当用户查询任务列表时，以文字形式回复。""",
        "output": "json"
    },
    "writing": {
        "name": "写作助手",
        "prompt": """你是一个专业写作助手，擅长各种文体。
用户可以指定写作风格（正式/轻松/文艺/幽默）。
默认风格：轻松自然。""",
        "output": "text"
    },
    "tutor": {
        "name": "学习导师",
        "prompt": """你是一位耐心细致的学习导师，擅长 Python 和 AI 领域。
根据学员水平调整讲解深度，多用类比和例子。
遇到学员不理解时，换一种方式解释。""",
        "output": "text"
    }
}

# ── 纯模型意图分类（无关键词规则）─────────────────────────────
def detect_intent(user_input: str) -> str:
    """仅返回角色标识：qa / task / writing / tutor"""
    classify_prompt = """请判断用户需求所属类型，严格只返回下面四个单词之一，不要额外解释、标点、换行：
qa = 普通知识问答、常识咨询、问题解答
task = 制定任务、待办、日程、计划、事务管理
writing = 创作文章、文案、故事、诗歌、总结、润色、各类文本撰写
tutor = 编程、Python、代码、算法、技术学习、知识点讲解教学

用户内容："""
    resp = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "user", "content": classify_prompt + user_input}],
        temperature=0.0,
        max_tokens=5
    )
    intent = resp.choices[0].message.content.strip().lower()
    return intent if intent in ROLES else "qa"


# ── 对话摘要压缩函数 ──────────────────────────────
def summarize_messages(messages: list[dict]) -> str:
    """把一段历史消息压缩为一句话核心摘要"""
    if not messages:
        return ""
    conv_text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
    prompt = f"""请把下面对话历史压缩成一句话核心摘要，保留关键信息，不要多余描述：
{conv_text}"""
    resp = client.chat.completions.create(
        model="qwen-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=100
    )
    return resp.choices[0].message.content.strip()


class PersonalAI:
    def __init__(self):
        self.current_role = "qa"
        self.histories: dict[str, list] = {role_id: [] for role_id in ROLES}
        self.summaries: dict[str, str] = {role_id: "" for role_id in ROLES}
        self.tasks: list[dict] = []
        self.turn_counts: dict[str, int] = {role_id: 0 for role_id in ROLES}

        # 压缩参数：保留最近 6 轮原始对话，超过则压缩旧历史
        self.recent_turns = 6
        self.summary_trigger = 12  # 累计12轮触发一次整体压缩

    def switch(self, role_id: str):
        if role_id not in ROLES:
            print(f"无效角色ID，可选：{', '.join(ROLES.keys())}")
            return
        self.current_role = role_id
        print(f"✓ 已切换到【{ROLES[role_id]['name']}】")

    def _maybe_compress(self, role_id: str):
        """对指定角色的历史做压缩：旧历史→摘要，保留最近N轮原始消息"""
        history = self.histories[role_id]
        if len(history) < self.summary_trigger:
            return  # 未到触发轮数，不压缩

        # 拆分：前面的旧消息 + 最近保留的消息
        old_messages = history[:-self.recent_turns]
        recent_messages = history[-self.recent_turns:]

        # 生成新摘要（叠加到旧摘要上）
        if old_messages:
            new_summary = summarize_messages(old_messages)
            if self.summaries[role_id]:
                self.summaries[role_id] += " " + new_summary
            else:
                self.summaries[role_id] = new_summary
            # 打印本次生成的新摘要
            print(f"\n📝 本次新增对话摘要：{new_summary}")

        # 只保留最近轮
        self.histories[role_id] = recent_messages

    # 新增：查看当前角色摘要
    def show_summary(self):
        current_sum = self.summaries[self.current_role]
        role_name = ROLES[self.current_role]["name"]
        print(f"\n=== 【{role_name}】对话摘要 ===")
        if not current_sum:
            print("暂无历史摘要")
        else:
            print(current_sum)

    def chat(self, user_input: str) -> str:
        # 纯模型自动识别并切换角色
        auto_role = detect_intent(user_input)
        if auto_role != self.current_role:
            self.switch(auto_role)

        role = ROLES[self.current_role]
        history = self.histories[self.current_role]
        summary = self.summaries[self.current_role]

        history.append({"role": "user", "content": user_input})

        # 组装消息：系统prompt + 历史摘要 + 最近原始对话
        messages = [{"role": "system", "content": role["prompt"]}]
        if summary:
            messages.append({"role": "system", "content": f"[历史摘要] {summary}"})
        messages.extend(history)

        kwargs = {"model": "qwen-turbo", "messages": messages}
        if role["output"] == "json":
            kwargs["response_format"] = {"type": "json_object"}

        response = client.chat.completions.create(**kwargs)
        reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": reply})

        # 任务数据保存
        if self.current_role == "task":
            try:
                task_data = json.loads(reply)
                if "task_name" in task_data:
                    task_data["created_at"] = datetime.now().strftime("%m-%d %H:%M")
                    task_data["id"] = len(self.tasks) + 1
                    self.tasks.append(task_data)
            except (json.JSONDecodeError, KeyError):
                pass

        # 检查是否需要压缩历史
        self._maybe_compress(self.current_role)

        self.turn_counts[self.current_role] += 1
        return reply

    def show_tasks(self):
        if not self.tasks:
            print("暂无任务")
            return
        print("\n=== 任务列表 ===")
        for t in self.tasks:
            deadline = t.get('deadline') or '无截止日期'
            print(f"  [{t['id']}] {t['task_name']} | {t.get('priority','中')}优先 | {deadline}")

    def status(self):
        print(f"\n当前角色：【{ROLES[self.current_role]['name']}】")
        print(f"任务数量：{len(self.tasks)}")
        for rid, count in self.turn_counts.items():
            if count > 0:
                print(f"  {ROLES[rid]['name']}: {count} 轮对话")
        # 显示摘要长度
        for rid, s in self.summaries.items():
            if s:
                print(f"  {ROLES[rid]['name']} 摘要长度: {len(s)} 字符")


def main():
    ai = PersonalAI()
    print("PersonalAI 启动！输入 /help 查看命令\n")

    # 新增 /summary 查看摘要命令
    COMMANDS = {
        "/qa":      ("切换知识助手",    lambda: ai.switch("qa")),
        "/task":    ("切换任务管家",    lambda: ai.switch("task")),
        "/write":   ("切换写作助手",    lambda: ai.switch("writing")),
        "/tutor":   ("切换学习导师",    lambda: ai.switch("tutor")),
        "/tasks":   ("查看任务列表",    lambda: ai.show_tasks()),
        "/summary": ("查看当前摘要",    lambda: ai.show_summary()),
        "/status":  ("查看系统状态",    lambda: ai.status()),
        "/quit":    ("退出",           lambda: exit(0)),
    }

    while True:
        user_input = input(f"\n[{ROLES[ai.current_role]['name']}] > ").strip()
        if not user_input:
            continue

        if user_input in COMMANDS:
            desc, action = COMMANDS[user_input]
            action()
            continue

        if user_input == "/help":
            for cmd, (desc, _) in COMMANDS.items():
                print(f"  {cmd:12} {desc}")
            continue

        reply = ai.chat(user_input)

        if ROLES[ai.current_role]["output"] == "json":
            try:
                data = json.loads(reply)
                print(json.dumps(data, ensure_ascii=False, indent=2))
            except json.JSONDecodeError:
                print(reply)
        else:
            print(f"\n{reply}")

if __name__ == "__main__":
    main()