import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 设置中文字体（Windows）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ===================== 生成具有现实意义的聚类数据 =====================
print("=" * 50)
print("无监督学习：电商用户分层聚类")
print("特征：年消费金额(万元)、月均购买次数、平均客单价(百元)")

# 生成模拟数据：3个特征，4个用户群体
n_samples = 500
n_features = 3
n_clusters = 4

X, _ = make_blobs(n_samples=n_samples, n_features=n_features, centers=n_clusters,
                  cluster_std=1.2, random_state=42)

# 映射到有实际意义的范围
# 年消费金额：0.5 ~ 20 万元
X[:, 0] = np.interp(X[:, 0], (X[:, 0].min(), X[:, 0].max()), (0.5, 20))
# 月均购买次数：0 ~ 30 次
X[:, 1] = np.interp(X[:, 1], (X[:, 1].min(), X[:, 1].max()), (0, 30))
# 平均客单价：0.5 ~ 8 百元（即 50 ~ 800 元）
X[:, 2] = np.interp(X[:, 2], (X[:, 2].min(), X[:, 2].max()), (0.5, 8))

# 对部分特征取整，使其更符合现实
X[:, 0] = np.round(X[:, 0], 1)   # 年消费保留1位小数
X[:, 1] = np.round(X[:, 1]).astype(int)  # 购买次数为整数
X[:, 2] = np.round(X[:, 2], 1)   # 客单价保留1位小数

print(f"数据形状: {X.shape}")
print("前5条样本（年消费/万, 月购买次数, 客单价/百元）:")
print(X[:5])

# ===================== 数据标准化 =====================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ===================== 肘部法则确定最佳k值 =====================
inertias = []
K_range = range(1, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(K_range, inertias, 'bo-')
plt.xlabel('k')
plt.ylabel('惯性(SSE)')
plt.title('肘部法则确定最佳k值')
plt.grid(True, alpha=0.3)

# ===================== 聚类（使用k=4） =====================
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)

# 获取聚类中心（原始尺度）
centers_orig = kmeans.cluster_centers_ * scaler.scale_ + scaler.mean_
centers_orig[:, 0] = np.round(centers_orig[:, 0], 1)
centers_orig[:, 1] = np.round(centers_orig[:, 1]).astype(int)
centers_orig[:, 2] = np.round(centers_orig[:, 2], 1)

# ===================== 可视化：选择两个主要特征展示 =====================
plt.subplot(1, 2, 2)
colors = ['red', 'blue', 'green', 'orange']
for i in range(n_clusters):
    mask = labels == i
    plt.scatter(X[mask, 0], X[mask, 1], c=colors[i], label=f'用户群{i}', alpha=0.6)
# 绘制聚类中心
plt.scatter(centers_orig[:, 0], centers_orig[:, 1], marker='X', s=200, c='black', label='聚类中心')
plt.xlabel('年消费金额 (万元)')
plt.ylabel('月均购买次数')
plt.title('用户分群 (年消费 vs 购买次数)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ===================== 特征组合散点图矩阵 =====================
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
feat_names = ['年消费金额(万元)', '月均购买次数', '平均客单价(百元)']

# 两两特征组合
pairs = [(0, 1), (0, 2), (1, 2)]
pair_titles = ['年消费 vs 购买次数', '年消费 vs 客单价', '购买次数 vs 客单价']
for idx, (i, j) in enumerate(pairs):
    ax = axes[0, idx]
    for cluster_id in range(n_clusters):
        mask = labels == cluster_id
        ax.scatter(X[mask, i], X[mask, j], c=colors[cluster_id], label=f'群{cluster_id}', alpha=0.6, s=30)
        # 聚类中心
        ax.scatter(centers_orig[cluster_id, i], centers_orig[cluster_id, j], 
                   marker='X', s=200, c=colors[cluster_id], edgecolors='black', linewidth=2)
    ax.set_xlabel(feat_names[i])
    ax.set_ylabel(feat_names[j])
    ax.set_title(pair_titles[idx])
    ax.legend()
    ax.grid(True, alpha=0.3)

# 每个特征的直方图（按簇着色）
for i in range(3):
    ax = axes[1, i]
    for cluster_id in range(n_clusters):
        mask = labels == cluster_id
        ax.hist(X[mask, i], bins=15, alpha=0.5, color=colors[cluster_id], 
                label=f'群{cluster_id}', edgecolor='black')
    ax.set_xlabel(feat_names[i])
    ax.set_ylabel('频数')
    ax.set_title(f'{feat_names[i]} 分布')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.suptitle('电商用户聚类详细分析', fontsize=16)
plt.tight_layout()
plt.show()

# ===================== 输出各簇统计信息 =====================
print("\n各用户群的统计特征：")
for i in range(n_clusters):
    cluster_data = X[labels == i]
    print(f"\n用户群 {i}: 人数 = {len(cluster_data)}")
    print(f"  平均年消费: {cluster_data[:,0].mean():.1f} 万元")
    print(f"  平均月购买次数: {cluster_data[:,1].mean():.1f} 次")
    print(f"  平均客单价: {cluster_data[:,2].mean():.1f} 百元")

# ===================== 现实意义解读 =====================
print("\n" + "=" * 50)
print("现实意义解读（示例）:")
for i in range(n_clusters):
    spend = np.mean(X[labels == i, 0])
    freq = np.mean(X[labels == i, 1])
    price = np.mean(X[labels == i, 2])
    if spend > 10 and freq > 15:
        desc = "高价值活跃用户"
    elif spend > 10 and freq <= 10:
        desc = "高价值低频用户（奢侈品倾向）"
    elif spend <= 5 and freq > 20:
        desc = "低价值高频用户（日常小商品）"
    else:
        desc = "普通用户"
    print(f"用户群 {i}: {desc}")