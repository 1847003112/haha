"""验证两个模型能被实际加载（本地离线，不联网）。"""
import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ["HF_HOME"] = str(ROOT / "SmartQuery" / "model" / ".cache" / "huggingface")
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_OFFLINE"] = "1"  # 强制离线，确认不依赖网络

print("[check] 加载 bge-m3 (稀疏+稠密) ...", flush=True)
t0 = time.time()
from FlagEmbedding import BGEM3FlagModel  # noqa: E402
m3 = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)
print(f"[check] bge-m3 加载成功 ({time.time() - t0:.1f}s)", flush=True)

print("[check] 加载 bge-reranker-v2-m3 ...", flush=True)
t0 = time.time()
from sentence_transformers import CrossEncoder  # noqa: E402
reranker = CrossEncoder("BAAI/bge-reranker-v2-m3", local_files_only=True)
print(f"[check] bge-reranker 加载成功 ({time.time() - t0:.1f}s)", flush=True)

# 跑一次小样本，确认能正常推理
print("[check] bge-m3 试编码 ...", flush=True)
out = m3.encode(["测试"], return_sparse=True, return_dense=False)
print(f"[check] bge-m3 稀疏权重条数: {len(out['lexical_weights'][0])}", flush=True)

print("[check] reranker 试打分 ...", flush=True)
score = reranker.predict([["测试", "这是一段测试文本"]])
print(f"[check] reranker 分数: {score[0]:.4f}", flush=True)

print("[check] 全部通过 ✅", flush=True)
