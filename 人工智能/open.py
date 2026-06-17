# 加密解密
from openai import OpenAI
from datetime import datetime
# import os
# from dotenv import load_dotenv
# load_dotenv(override=True)
# api_key=os.getenv('QWEN_API_KEY')
# model=os.getenv('DEFAULT_MODEL','qwen-plus')
# print (f'使用的模型:{model}')
# from cryptography.fernet import Fernet
# key = Fernet.generate_key()
# print(f'加密密钥:{key.decode()}')
# f=Fernet(key)
# token=f.encrypt(b'my-secret-api-key-123')
# print(f'加密后:{token.decode()}')
# original_token=f.decrypt(token)
# print(f'解密后:{original_token.decode()}')
# with open('secret.key','wb') as f:
#     f.write(key)



def write_log(message: str):
    with open("open.log", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")
client = OpenAI(
    api_key="sk-aee853eb5fe34137b4800ef4561cdc15",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
system_prompt = input("请定义AI的系统人设:").strip()
messages = [{'role': "system", "content": system_prompt}]
write_log(f"系统人设已设置: {system_prompt}")

EXIT_COMMANDS = {"1"}
CLEAR_COMMANDS = {"2"}

while True:
    user_input = input("请输入: ")
    if not user_input:
        print("输入不能为空，请重新输入。")
        continue

    if user_input in EXIT_COMMANDS:
        print("再见！对话已结束。")
        write_log("用户主动退出对话")
        break

    if user_input in CLEAR_COMMANDS:
        messages = [messages[0]]   
        print("上下文已清空，机器人将不再记住之前的对话。")
        write_log("用户清空了对话上下文")
        continue

    # ========== 新功能：查看对话统计 ==========
    if user_input == "3":
        total_msgs = len(messages)
        user_msgs = sum(1 for m in messages if m["role"] == "user")
        assistant_msgs = sum(1 for m in messages if m["role"] == "assistant")
        system_exists = 1 if any(m["role"] == "system" for m in messages) else 0
        rounds = min(user_msgs, assistant_msgs)
        total_chars = sum(len(m["content"]) for m in messages)
        estimated_tokens = int(total_chars / 1.8)  # 粗略估算
        print("\n========== 对话统计 ==========")
        print(f"消息总数：{total_msgs} 条")
        print(f"  - 系统消息：{system_exists} 条")
        print(f"  - 用户消息：{user_msgs} 条")
        print(f"  - 助手消息：{assistant_msgs} 条")
        print(f"完整对话轮数：{rounds} 轮")
        print(f"总字符数：{total_chars}")
        print(f"预估 token 数：约 {estimated_tokens} tokens")
        print("================================\n")
        write_log(f"用户查看了对话统计：消息数={total_msgs}, 轮数={rounds}, 预估tokens={estimated_tokens}")
        continue
    # ======================================

    write_log(f"用户输入: {user_input}")
    messages.append({"role": "user", "content": user_input})

    stream = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
        stream=True,
        temperature=0.5
    )

    ans = ""
    print("助手回复:", end="")
    for chunk in stream:
        if chunk.choices[0].delta.content:
            ans += chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="")
    print()
    write_log(f"助手回复：{ans}")

    messages.append({"role": "assistant", "content": ans})
