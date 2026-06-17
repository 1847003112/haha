import json
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
# 加载 .env 环境变量（指定完整路径）
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

# ===================== 关键修改 =====================
# 密钥：从 .env 读取
ALIYUN_API_KEY = os.getenv("QWEN_API_KEY")  # 使用 QWEN_API_KEY 作为阿里云 API Key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GLM_API_KEY = os.getenv("GLM_API_KEY")

ALIYUN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
GLM_BASE_URL = "https://open.bigmodel.cn/api/paas/v4"
# ====================================================

class Debater:
    """辩手基类"""
    def __init__(self, name: str, model: str, api_key: str, base_url: str):
        self.name = name
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.history = []  # 本方所有发言

    def reply(self, topic: str, opponent_last_msg: str = None) -> str:
        system_prompt = (
            f"你是一位辩论高手，你的名字是{self.name}。"
            f"你需要在辩题「{topic}」下进行有力辩论。"
            "请保持逻辑清晰、论据充分，直接阐述观点，不要重复对方原话。"
            "每次发言控制在 100 字以内。"
        )
        messages = [{"role": "system", "content": system_prompt}]

        if opponent_last_msg is not None:
            messages.append({"role": "user", "content": f"对方刚才说：{opponent_last_msg}。请反驳并继续你的论证。"})
        else:
            messages.append({"role": "user", "content": f"请针对辩题「{topic}」发表你的开篇立论。"})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.8,
            max_tokens=300
        )
        content = response.choices[0].message.content
        self.history.append(content)
        return content


class AliyunDebater(Debater):
    def __init__(self, name):
        super().__init__(name, "qwen-plus", ALIYUN_API_KEY, ALIYUN_BASE_URL)


class DeepseekDebater(Debater):
    def __init__(self, name):
        super().__init__(name, "deepseek-chat", DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL)


class ZhipuDebater(Debater):
    def __init__(self, name):
        super().__init__(name, "glm-4-plus", GLM_API_KEY,GLM_BASE_URL)


class Judge:
    """裁判，使用第三个模型进行判决和打分"""
    def __init__(self, debater: Debater):
        self.debater = debater

    def evaluate(self, topic: str, debate_log: str) -> str:
        system_prompt = (
            "你是一位专业辩论裁判，请根据以下辩论记录，对双方表现进行评判。"
            "你需要输出：\n1. 整体评价（逻辑、论据、表达）\n"
            "2. 明确指出双方优缺点\n"
            "3. 最终获胜方及理由\n"
            "4. 给正方和反方分别打分（满分100分）\n"
            "请以 JSON 格式返回：{\"winner\": \"正方/反方\", "
            "\"score_positive\": 分数, \"score_negative\": 分数, "
            "\"comment\": \"详细评语\"}"
        )
        user_msg = f"辩题：{topic}\n\n完整辩论记录：\n{debate_log}"

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ]
        response = self.debater.client.chat.completions.create(
            model=self.debater.model,
            messages=messages,
            temperature=0.3,
            max_tokens=800
        )
        return response.choices[0].message.content


def run_debate(topic: str):
    # 正方：阿里云千问，反方：DeepSeek，裁判：智谱GLM
    debater_pro = AliyunDebater("阿里云千问")
    debater_con = DeepseekDebater("DeepSeek")
    judge_model = ZhipuDebater("裁判:智谱GLM")
    judge = Judge(judge_model)

    full_log = ""
    debate_rounds = []

    # 三轮辩论
    for r in range(1, 4):
        print(f"\n===== 第 {r} 轮 =====")

        # 正方发言
        pro_msg = debater_pro.reply(topic, debate_rounds[-1]["content"] if debate_rounds and debate_rounds[-1]["side"] == "negative" else None)
        print(f"{debater_pro.name}：{pro_msg}\n")
        full_log += f"第{r}轮 - {debater_pro.name}：{pro_msg}\n\n"
        debate_rounds.append({"round": r, "speaker": debater_pro.name, "side": "positive", "content": pro_msg})

        # 反方发言
        con_msg = debater_con.reply(topic, pro_msg)
        print(f"{debater_con.name}：{con_msg}\n")
        full_log += f"第{r}轮 - {debater_con.name}：{con_msg}\n\n"
        debate_rounds.append({"round": r, "speaker": debater_con.name, "side": "negative", "content": con_msg})

    # 裁判打分
    print("===== 裁判评判中... =====\n")
    verdict_raw = judge.evaluate(topic, full_log)

    # 解析裁判返回的 JSON
    try:
        # 提取 JSON 部分（移除可能的前后标记）
        verdict_clean = verdict_raw.replace('\n', ' ').replace('\r', ' ')
        import re
        json_match = re.search(r'\{.*\}', verdict_clean, re.DOTALL)
        if json_match:
            verdict_json = json.loads(json_match.group())
            
            # 根据分数确定获胜方（确保分数高的为获胜方）
            score_positive = verdict_json.get("score_positive", 0)
            score_negative = verdict_json.get("score_negative", 0)
            
            if score_positive > score_negative:
                winner = "正方"
            elif score_negative > score_positive:
                winner = "反方"
            else:
                winner = "平局"
            
            # 更新获胜方
            verdict_json["winner"] = winner
            
            # 格式化输出
            print("===== 🏆 辩论结果 =====\n")
            print(f"辩题：{topic}\n")
            print(f"正方（{debater_pro.name}）得分：{score_positive}分")
            print(f"反方（{debater_con.name}）得分：{score_negative}分")
            print(f"\n获胜方：{winner}")
            print(f"\n裁判评语：\n{verdict_json.get('comment', '')}\n")
            
            # 更新为修正后的 verdict
            verdict_clean = json.dumps(verdict_json, ensure_ascii=False, indent=2)
        else:
            print(verdict_clean)
    except Exception as e:
        print(f"解析裁判结果失败: {e}")
        print("原始裁判输出:", verdict_clean)

    # 保存记录
    record = {
        "topic": topic,
        "time": datetime.now().isoformat(),
        "debate_rounds": debate_rounds,
        "full_transcript": full_log,
        "judge_verdict": verdict_clean
    }

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_filename = f"debate_{timestamp}.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    # 纯文本版
    txt_filename = f"debate_{timestamp}.txt"
    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(f"辩题：{topic}\n\n")
        f.write(full_log)
        f.write(f"\n裁判判决：\n{verdict_clean}\n")

    print(f"\n辩论记录已保存至 {json_filename} 和 {txt_filename}")
    return record

if __name__ == "__main__":
    topic = input("请输入辩题：")
    run_debate(topic)