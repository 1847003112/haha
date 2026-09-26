"""预下载 bge-m3 与 bge-reranker-v2-m3 到项目 HF_HOME 目录。

用法：python scripts/download_models.py
下载完成后即可离线运行，无需再联网（配合 retriever.py 的 local_files_only=True）。
"""
import os
from pathlib import Path

# 与 .env 的 HF_HOME / HF_ENDPOINT 保持一致
ROOT = Path(__file__).resolve().parents[1]
HF_HOME = ROOT / "SmartQuery" / "model" / ".cache" / "huggingface"
os.environ["HF_HOME"] = str(HF_HOME)
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from huggingface_hub import snapshot_download  # noqa: E402

MODELS = ["BAAI/bge-m3", "BAAI/bge-reranker-v2-m3"]

# 只下模型文件，跳过示例图片 / .DS_Store 等无关文件（这些在镜像站上会 403）
IGNORE_PATTERNS = [
    "*.DS_Store", "**/.DS_Store",
    "imgs/**", "imgs/*", "images/**", "images/*",
    "*.png", "*.jpg", "*.jpeg", "*.webp", "*.gif", "*.bmp", "*.svg",
]

import time

for m in MODELS:
    print(f"[download] 开始下载 {m} ...", flush=True)
    for attempt in range(1, 6):  # 最多重试 5 次，断点续传
        try:
            path = snapshot_download(repo_id=m, ignore_patterns=IGNORE_PATTERNS)
            print(f"[download] 完成 {m} -> {path}", flush=True)
            break
        except Exception as e:
            print(f"[download] 第 {attempt} 次失败 {m}: {e}", flush=True)
            if attempt < 5:
                print(f"[download] 3 秒后重试 ...", flush=True)
                time.sleep(3)
            else:
                print(f"[download] {m} 重试耗尽，放弃", flush=True)

print("[download] 全部结束", flush=True)
