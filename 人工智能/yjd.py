import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_regression, make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import r2_score, mean_absolute_error, accuracy_score, confusion_matrix, ConfusionMatrixDisplay

# 设置中文字体（Windows）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ===================== 1. 回归：猪肉价格预测 =====================
print("=" * 50)
print("1. 回归任务：猪肉价格预测（基于饲料成本、疫情指数、新鲜程度）")

X_pork, y_pork = make_regression(n_samples=600, n_features=3, noise=10, random_state=42)

# 特征映射
X_pork[:, 0] = np.interp(X_pork[:, 0], (X_pork[:, 0].min(), X_pork[:, 0].max()), (2.5, 5.0))
X_pork[:, 0] = np.round(X_pork[:, 0], 2)
X_pork[:, 1] = np.interp(X_pork[:, 1], (X_pork[:, 1].min(), X_pork[:, 1].max()), (0, 1))
X_pork[:, 1] = np.round(X_pork[:, 1], 3)
X_pork[:, 2] = np.interp(X_pork[:, 2], (X_pork[:, 2].min(), X_pork[:, 2].max()), (1, 10))
X_pork[:, 2] = np.round(X_pork[:, 2]).astype(int)

y_pork = np.interp(y_pork, (y_pork.min(), y_pork.max()), (15, 45))
y_pork = np.round(y_pork, 1)

print(f"特征矩阵形状: {X_pork.shape}")
print("\n前5条样本（饲料成本, 疫情指数, 新鲜程度）:")
print(X_pork[:5])
print("对应猪肉价格（元/公斤）:", y_pork[:5])

X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(X_pork, y_pork, test_size=0.2, random_state=42)
rf_pork = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=6)
rf_pork.fit(X_train_p, y_train_p)
y_pred_p = rf_pork.predict(X_test_p)

print(f"\nR²: {r2_score(y_test_p, y_pred_p):.4f}")
print(f"MAE: {mean_absolute_error(y_test_p, y_pred_p):.2f} 元/公斤")

# 可视化回归
fig = plt.figure(figsize=(15, 10))
feat_names = ['饲料成本 (元/kg)', '疫情指数', '新鲜程度 (1-10)']
for i in range(3):
    ax = fig.add_subplot(2, 3, i+1)
    ax.hist(X_pork[:, i], bins=20, color='lightcoral', edgecolor='black')
    ax.set_title(feat_names[i])
    ax.grid(True, alpha=0.3)

ax = fig.add_subplot(2, 3, 4)
ax.scatter(y_test_p, y_pred_p, alpha=0.7, color='darkgreen')
ax.plot([y_test_p.min(), y_test_p.max()], [y_test_p.min(), y_test_p.max()], 'r--')
ax.set_xlabel("实际猪肉价格 (元/kg)")
ax.set_ylabel("预测猪肉价格 (元/kg)")
ax.set_title("实际值 vs 预测值")
ax.grid(True, alpha=0.3)

ax = fig.add_subplot(2, 3, 5)
importance = rf_pork.feature_importances_
ax.barh(feat_names, importance, color='orange')
ax.set_title("特征重要性")
ax.set_xlabel("重要度")

ax = fig.add_subplot(2, 3, 6)
residuals = y_test_p - y_pred_p
ax.hist(residuals, bins=20, color='purple', alpha=0.7)
ax.axvline(0, color='red', linestyle='--')
ax.set_title("残差分布")
ax.set_xlabel("残差 (元/kg)")
plt.tight_layout()
plt.show()

# 特征与价格散点图
fig2, axes = plt.subplots(1, 3, figsize=(15, 5))
for i in range(3):
    axes[i].scatter(X_pork[:, i], y_pork, alpha=0.5, c='blue')
    axes[i].set_xlabel(feat_names[i])
    axes[i].set_ylabel("猪肉价格 (元/kg)")
    axes[i].grid(True, alpha=0.3)
plt.suptitle("各特征与猪肉价格的关系")
plt.tight_layout()
plt.show()

# ===================== 2. 分类：客户购买意向预测 =====================
print("\n" + "=" * 50)
print("2. 分类任务：客户购买意向预测")
X_clf, y_clf = make_classification(n_samples=800, n_features=3, n_informative=3, n_redundant=0,
                                    n_clusters_per_class=1, flip_y=0.05, random_state=42)
X_clf[:, 0] = np.interp(X_clf[:, 0], (X_clf[:, 0].min(), X_clf[:, 0].max()), (20, 60))
X_clf[:, 1] = np.interp(X_clf[:, 1], (X_clf[:, 1].min(), X_clf[:, 1].max()), (3, 15))
X_clf[:, 2] = np.interp(X_clf[:, 2], (X_clf[:, 2].min(), X_clf[:, 2].max()), (0, 20))
X_clf[:, 2] = np.round(X_clf[:, 2]).astype(int)

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_clf, y_clf, test_size=0.2, random_state=42)
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
rf_clf.fit(X_train_c, y_train_c)
y_pred_c = rf_clf.predict(X_test_c)
print(f"准确率: {accuracy_score(y_test_c, y_pred_c):.4f}")

fig_clf = plt.figure(figsize=(15, 8))
feat_names_clf = ['年龄', '年收入(万)', '月均购物次数']
for i in range(3):
    ax = fig_clf.add_subplot(2, 3, i+1)
    for label in [0, 1]:
        mask = y_clf == label
        ax.hist(X_clf[mask, i], bins=15, alpha=0.5, label=f'未购买' if label==0 else '购买', edgecolor='black')
    ax.set_title(feat_names_clf[i])
    ax.legend()
    ax.grid(True, alpha=0.3)

cm = confusion_matrix(y_test_c, y_pred_c)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['未购买', '购买'])
disp.plot(ax=fig_clf.add_subplot(2, 3, 4), cmap='Blues')
fig_clf.axes[3].set_title("混淆矩阵")

ax = fig_clf.add_subplot(2, 3, 5)
importance_clf = rf_clf.feature_importances_
ax.bar(feat_names_clf, importance_clf, color='teal')
ax.set_title("特征重要性")
plt.tight_layout()
plt.show()