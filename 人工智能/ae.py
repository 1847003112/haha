import os, sys, random
from dotenv import load_dotenv
import pymysql
from pymysql.cursors import DictCursor
from openai import OpenAI

# ========== 直接配置 ==========
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'word_tool',
    'port': 3306,
    'charset': 'utf8mb4'
}
WORDS_FILE = 'words.txt'
QUIZ_SIZE = 5
SCORE_PER_QUESTION = 10

# 大模型配置（URL和模型写在此处）
LLM_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
LLM_MODEL = "qwen-plus"

# ========== 读取API密钥 ==========
load_dotenv()
LLM_API_KEY = os.getenv('QWEN_API_KEY', '')

# ========== 数据库操作 ==========
def get_db_connection():
    return pymysql.connect(**DB_CONFIG, cursorclass=DictCursor)

def save_study_record(english, chinese, is_correct):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO study_records (english, chinese, is_correct) VALUES (%s, %s, %s)",
                   (english, chinese, is_correct))
    conn.commit()
    cursor.close()
    conn.close()

def add_or_update_wrong_word(english, chinese):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE wrong_words SET wrong_count = wrong_count + 1 WHERE english = %s", (english,))
    if cursor.rowcount == 0:
        cursor.execute("INSERT INTO wrong_words (english, chinese) VALUES (%s, %s)", (english, chinese))
    conn.commit()
    cursor.close()
    conn.close()

def get_wrong_words(limit=50):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT english, chinese, wrong_count FROM wrong_words ORDER BY wrong_count DESC LIMIT %s", (limit,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def remove_wrong_word(english):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM wrong_words WHERE english = %s", (english,))
    conn.commit()
    cursor.close()
    conn.close()

# ========== 大模型辅助 ==========
def generate_example_and_tip(word_en, word_cn):
    if not LLM_API_KEY:
        return "（未配置API Key，请在.env中设置QWEN_API_KEY）"
    client = OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)
    prompt = f"请为英文单词 \"{word_en}\"（中文：{word_cn}）生成：\n1. 一个实用的英文例句并给出中文翻译\n2. 一条记忆技巧\n\n输出格式：\n例句：...\n例句翻译：...\n记忆技巧：..."
    try:
        resp = client.chat.completions.create(model=LLM_MODEL, messages=[{"role":"user","content":prompt}], temperature=0.7, max_tokens=300)
        return resp.choices[0].message.content
    except Exception as e:
        return f"（生成失败：{e}）"

# ========== 核心类 ==========
class VocabTrainer:
    def __init__(self):
        self.words = self.load_words(WORDS_FILE)
        self.score = 0
        self.total = 0

    def load_words(self, path):
        if not os.path.exists(path):
            print(f"错误：单词库文件 {path} 不存在！请创建该文件，每行格式：英文,中文")
            sys.exit(1)
        words = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or ',' not in line: continue
                en, cn = line.split(',', 1)
                words.append({"en": en.strip(), "cn": cn.strip()})
        if not words:
            print(f"错误：{path} 中没有有效单词")
            sys.exit(1)
        return words

    def ask_question(self, word):
        print(f"\n📖 中文：{word['cn']}")
        inp = input("请输入英文（1退出）：").strip().lower()
        if inp == '1':
            print("返回上一级菜单")
            return None  # 返回 None 表示用户要退出
        correct = (inp == word['en'].lower())
        self.total += 1
        if correct:
            self.score += SCORE_PER_QUESTION
            print(f"✅ 正确！ +{SCORE_PER_QUESTION}分  总分：{self.score}")
        else:
            print(f"❌ 错误！ 正确答案：{word['en']}  总分：{self.score}")
            # 答错时自动显示学习提示
            print("\n📚 学习提示：")
            print(generate_example_and_tip(word['en'], word['cn']))
            print("-----------------------------------")
            add_or_update_wrong_word(word['en'], word['cn'])
        save_study_record(word['en'], word['cn'], 1 if correct else 0)
        return correct

    def normal_practice(self, count):
        if count > len(self.words): count = len(self.words)
        for w in random.sample(self.words, count):
            result = self.ask_question(w)
            if result is None:  # 用户选择退出
                break
        print(f"\n🎉 练习结束！ 得分：{self.score}/{count*SCORE_PER_QUESTION}")

    def review_wrong_words(self):
        wrongs = get_wrong_words(50)
        if not wrongs:
            print("🎉 错题本为空！")
            return
        print(f"\n📘 开始复习 {len(wrongs)} 个错题")
        review_score = 0
        for item in wrongs:
            w = {"en": item['english'], "cn": item['chinese']}
            print(f"\n--- 复习（已错 {item['wrong_count']} 次） ---")
            result = self.ask_question(w)
            if result is None:  # 用户选择退出
                break
            if result:
                remove_wrong_word(w['en'])
                review_score += SCORE_PER_QUESTION
                print("🎉 已从错题本清除！")
            else:
                print("💪 继续努力")
        print(f"\n复习额外加分：{review_score}")
        self.score += review_score

    def show_stats(self):
        print(f"\n📊 本次会话：答题{self.total}，得分{self.score}")

    def menu(self):
        while True:
            print("\n" + "="*40)
            print("1. 随机练习\n2. 复习错题本\n3. 查看成绩\n4. 退出")
            ch = input("请选择(1-4)：").strip()
            if ch == '1':
                n = input(f"数量（默认{QUIZ_SIZE}）：").strip()
                self.normal_practice(int(n) if n.isdigit() else QUIZ_SIZE)
            elif ch == '2':
                self.review_wrong_words()
            elif ch == '3':
                self.show_stats()
            elif ch == '4':
                print("再见！")
                break
            else:
                print("无效输入")

# ========== 主函数 ==========
def main():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM study_records LIMIT 1")
        cursor.execute("SELECT 1 FROM wrong_words LIMIT 1")
        cursor.close()
        conn.close()
    except pymysql.Error as e:
        print("数据库错误：请先创建数据库和表，SQL如下：")
        print("""
CREATE DATABASE IF NOT EXISTS word_tool;
USE word_tool;
CREATE TABLE study_records (id INT AUTO_INCREMENT PRIMARY KEY, english VARCHAR(50) NOT NULL, chinese VARCHAR(100) NOT NULL, is_correct TINYINT NOT NULL, create_time DATETIME DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE wrong_words (id INT AUTO_INCREMENT PRIMARY KEY, english VARCHAR(50) NOT NULL UNIQUE, chinese VARCHAR(100) NOT NULL, wrong_count INT DEFAULT 1);
        """)
        print(f"具体错误：{e}")
        sys.exit(1)
    trainer = VocabTrainer()
    print("🐾 智能背单词工具")
    print("提示：答错时会自动显示学习提示。")
    trainer.menu()

if __name__ == "__main__":
    main()