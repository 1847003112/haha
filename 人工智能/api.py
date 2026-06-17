import sys
import os
import json
from datetime import datetime
from pathlib import Path
from cryptography.fernet import Fernet
from openai import OpenAI, APIConnectionError

# 确保标准输出编码为 UTF-8（防止 Windows 等环境乱码）
sys.stdout.reconfigure(encoding='utf-8')


def write_log(message: str):
    """写入日志文件"""
    with open("open.log", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")


class SecretManager:
    """
    基于 Fernet 的密钥管理器
    功能：
        - 生成/加载主密钥（存储于 .secret.key 文件）
        - 加密多平台的 API Key 并保存到 api_keys.enc 文件
        - 解密并返回指定平台的 API Key
    """

    CONFIG_DIR = Path.home() / ".llm_tool"
    KEY_FILE = CONFIG_DIR / ".secret.key"
    DATA_FILE = CONFIG_DIR / "api_keys.enc"

    def __init__(self):
        self._ensure_config_dir()
        self._cipher = self._load_or_create_key()

    def _ensure_config_dir(self):
        """确保配置目录存在"""
        self.CONFIG_DIR.mkdir(exist_ok=True, mode=0o700)

    def _load_or_create_key(self) -> Fernet:
        """加载已有密钥，若不存在则生成新密钥"""
        if self.KEY_FILE.exists():
            with open(self.KEY_FILE, "rb") as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.KEY_FILE, "wb") as f:
                f.write(key)
            os.chmod(self.KEY_FILE, 0o600)
        return Fernet(key)

    def _load_encrypted_data(self) -> dict:
        """加载加密存储的 API Keys 文件，若不存在则返回空字典"""
        if not self.DATA_FILE.exists():
            return {}
        with open(self.DATA_FILE, "rb") as f:
            encrypted_data = f.read()
        try:
            decrypted = self._cipher.decrypt(encrypted_data)
            return json.loads(decrypted.decode("utf-8"))
        except Exception as e:
            raise RuntimeError("解密 API Keys 文件失败，可能密钥已损坏") from e

    def _save_encrypted_data(self, data: dict):
        """将 API Keys 字典加密后保存到文件"""
        json_str = json.dumps(data, indent=2)
        encrypted = self._cipher.encrypt(json_str.encode("utf-8"))
        with open(self.DATA_FILE, "wb") as f:
            f.write(encrypted)
        os.chmod(self.DATA_FILE, 0o600)

    def set_api_key(self, platform: str, api_key: str):
        """加密保存某个平台的 API Key"""
        data = self._load_encrypted_data()
        data[platform] = api_key
        self._save_encrypted_data(data)

    def get_api_key(self, platform: str) -> str:
        """获取指定平台的明文 API Key"""
        data = self._load_encrypted_data()
        if platform not in data:
            raise KeyError(f"平台 '{platform}' 的 API Key 未设置，请先使用 set_api_key 方法保存")
        return data[platform]

    def list_platforms(self):
        """列出已存储 API Key 的平台"""
        return list(self._load_encrypted_data().keys())


class LLM:
    """多平台 LLM 调用器，内部自动通过 SecretManager 获取加密的 API Key"""

    PLATFORMS = {
        "deepseek": {
            "base_url": "https://api.deepseek.com/v1",
            "model": "deepseek-chat",
        },
        "qwen": {
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "model": "qwen-plus",
        },
        "glm": {
            "base_url": "https://open.bigmodel.cn/api/paas/v4",
            "model": "glm-5.1",
        }
    }

    def __init__(self, platform: str):
        """
        :param platform: 平台名称，需在 PLATFORMS 中定义
        """
        if platform not in self.PLATFORMS:
            raise ValueError(f"不支持的平台: {platform}，可选: {list(self.PLATFORMS.keys())}")

        secret_mgr = SecretManager()
        api_key = secret_mgr.get_api_key(platform)

        config = self.PLATFORMS[platform]
        self.client = OpenAI(
            api_key=api_key,
            base_url=config["base_url"],
        )
        self.model = config["model"]
        self.temperature = 0.5
        self.platform = platform
        self.stream = True

    def chat_with_messages(self, messages: list) -> str:
        """
        发送多轮对话消息（包含 system、user、assistant 等），返回模型完整回复
        同时将流式输出逐字打印到控制台（保持与原体验一致）
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                stream=self.stream,
            )
            if self.stream:
                full_content = ""
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_content += content
                        print(content, end="")
                print()  # 换行
                return full_content
            else:
                return response.choices[0].message.content
        except APIConnectionError:
            error_msg = f"网络连接失败：无法连接到 {self.platform} API，请检查网络连接或稍后重试。"
            print(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"请求失败：{str(e)}"
            print(error_msg)
            return error_msg


def get_or_set_api_key(platform: str, secret_mgr: SecretManager) -> bool:
    """检查指定平台是否已有 API Key，若无则提示用户输入并保存；返回是否成功获取"""
    try:
        _ = secret_mgr.get_api_key(platform)
        print(f"✓ 已从加密存储中加载 {platform} 的 API Key")
        return True
    except KeyError:
        print(f"未找到 {platform} 的 API Key，请手动输入：")
        api_key = input(">>> ").strip()
        if not api_key:
            print("API Key 不能为空，请重新运行程序并输入有效密钥。")
            return False
        secret_mgr.set_api_key(platform, api_key)
        print(f"✓ {platform} API Key 已加密保存")
        return True


def main():
    print("=== 多平台 LLM 对话工具 (加密 API Key) ===\n")

    # 1. 初始化密钥管理器
    secret_mgr = SecretManager()

    # 2. 选择平台
    platforms = list(LLM.PLATFORMS.keys())
    print("可用平台：")
    for idx, name in enumerate(platforms, 1):
        print(f"  {idx}. {name}")
    while True:
        choice = input("请选择平台 (输入编号或名称): ").strip().lower()
        if choice.isdigit() and 1 <= int(choice) <= len(platforms):
            platform = platforms[int(choice) - 1]
            break
        elif choice in platforms:
            platform = choice
            break
        else:
            print("输入无效，请重新选择。")

    # 3. 获取该平台的 API Key（加密存储）
    if not get_or_set_api_key(platform, secret_mgr):
        return

    # 4. 创建 LLM 实例
    llm = LLM(platform)
    print(f"\n已切换到 {platform} 模型：{llm.model}\n")

    # 5. 设置系统人设
    system_prompt = input("请定义 AI 的系统人设: ").strip()
    if not system_prompt:
        system_prompt = "你是一个有用的助手。"
    messages = [{"role": "system", "content": system_prompt}]
    write_log(f"系统人设已设置: {system_prompt}")

    # 6. 对话控制命令
    EXIT_COMMANDS = {"1"}
    CLEAR_COMMANDS = {"2"}
    STATS_COMMAND = "3"

    print("\n对话已开始。输入 1 退出，输入 2 清空上下文，输入 3 查看统计信息。")

    while True:
        user_input = input("\n请输入: ").strip()
        if not user_input:
            print("输入不能为空，请重新输入。")
            continue

        if user_input in EXIT_COMMANDS:
            print("再见！对话已结束。")
            write_log("用户主动退出对话")
            break

        if user_input in CLEAR_COMMANDS:
            messages = [messages[0]]   # 保留 system 消息
            print("上下文已清空，机器人将不再记住之前的对话。")
            write_log("用户清空了对话上下文")
            continue

        if user_input == STATS_COMMAND:
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

        # 正常对话
        write_log(f"用户输入: {user_input}")
        messages.append({"role": "user", "content": user_input})

        print("助手回复: ", end="")
        ans = llm.chat_with_messages(messages)

        write_log(f"助手回复：{ans}")
        messages.append({"role": "assistant", "content": ans})


if __name__ == "__main__":
    main()