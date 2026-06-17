# from sklearn.datasets import load_iris
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.linear_model import LogisticRegression
# from sklearn.pipeline import make_pipeline
# from sklearn.metrics import accuracy_score
# import matplotlib.pyplot as plt

# # 2. 加载数据
# iris = load_iris(); X = iris.data; y = iris.target

# # 新增：数据可视化 - 萼片长度 vs 花瓣长度散点图
# plt.figure(figsize=(10, 6)); colors = ['red', 'green', 'blue']
# for i, c in enumerate(colors): plt.scatter(X[y==i,0], X[y==i,2], c=c, label=iris.target_names[i], edgecolor='k', s=50)
# plt.xlabel('Sepal Length'); plt.ylabel('Petal Length'); plt.title('Iris Dataset'); plt.legend(); plt.show()

# # 3. 划分训练集/测试集; 4. 构建并训练Pipeline模型
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
# pipe = make_pipeline(StandardScaler(), LogisticRegression()); pipe.fit(X_train, y_train)

# # 5. 预测与评估
# y_pred = pipe.predict(X_test); accuracy = accuracy_score(y_test, y_pred)
# print(f"模型在测试集上的准确率: {accuracy:.4f}")
# --------------------------------------------------------
# from sklearn.datasets import load_iris
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import accuracy_score
# import matplotlib.pyplot as plt

# # 1. 加载数据
# iris = load_iris()
# X = iris.data
# y = iris.target

# # 2. 数据可视化：萼片长度 vs 花瓣长度散点图
# # plt.figure(figsize=(10, 6))
# # colors = ['red', 'green', 'blue']
# # for i, c in enumerate(colors):
# #     plt.scatter(X[y==i, 0], X[y==i, 2], c=c, label=iris.target_names[i], edgecolor='k', s=50)
# # plt.xlabel('Sepal Length')
# # plt.ylabel('Petal Length')
# # plt.title('Iris Dataset')
# # plt.legend()
# # plt.show()

# # 3. 划分训练集和测试集
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42,stratify=y)

# # 4. 特征标准化（不使用 pipeline，手动两步）
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)   # 在训练集上拟合并转换
# X_test_scaled = scaler.transform(X_test)         # 用训练集的参数转换测试集

# # 5. 训练逻辑回归模型
# model = LogisticRegression(random_state=42,max_iter=200)
# model.fit(X_train_scaled, y_train)

# # 6. 预测与评估
# y_train_pred = model.predict(X_train_scaled)
# y_test_pred=model.predict(X_test_scaled)
# train_acc=accuracy_score(y_train,y_train_pred)
# test_acc=accuracy_score(y_test,y_test_pred)
# print(f"模型在测试集上的准确率: {test_acc:.4f}")
# print(f"模型在训练集上的准确率: {train_acc:.4f}")
# ------------------------------------------------------
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression

# np.random.seed(42)
# area = np.random.randint(50, 150, size=100)
# price = 1.2 * area + 10 + np.random.normal(0, 10, size=100)
# x = area.reshape(-1, 1)
# y = price
# plt.figure(figsize=(10, 6))
# plt.scatter(area, price, alpha=0.7, color='skyblue', label='Data Points')
# plt.xlabel('Area (sq.m.)')
# plt.ylabel('Price (10000 yuan)')
# plt.title('House Area vs. Price')
# plt.legend()
# plt.grid(True)

# # 后续训练等代码正常执行
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
# model = LinearRegression()
# model.fit(x_train, y_train)
# print(f'模型斜率(m): {model.coef_[0]:.4f}')
# print(f'模型截距(b): {model.intercept_:.4f}')
# y_pred=model.predict(x_test)
# plt.plot(x_test,y_pred,color='red',label='Predicted Price')
# # plt.show()
# from sklearn.metrics import mean_absolute_error,r2_score
# y_pred=model.predict(x_test)
# mae=mean_absolute_error(y_test,y_pred)
# r2=r2_score(y_test,y_pred)
# print(f'在测试集上的平均绝对误差(MAE):{mae:.4f}(万元)')
# print(f'在测试集上的决定系数(R^2):{r2:.4f}')
# from sklearn.ensemble import RandomForestRegressor
# rf_model=RandomForestRegressor(n_estimators=100,random_state=42)
# rf_model.fit(x_train,y_train)
# y_pred_rf=rf_model.predict(x_test)
#------------------------------------------------------------------------
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.datasets import load_iris
# from sklearn.preprocessing import StandardScaler
# from sklearn.cluster import KMeans
# plt.rcParams['font.sans-serif']=['SimHei']
# plt.rcParams['axes.unicode_minus']=False
# iris=load_iris()
# X=iris.data
# scaler=StandardScaler()
# X_scaled=scaler.fit_transform(X)
# kmeans=KMeans(n_clusters=4,random_state=42)
# kmeans.fit(X_scaled)
# y_pred=kmeans.fit_predict(X_scaled)
# print("聚类中心点:",kmeans.cluster_centers_)
# plt.scatter(X_scaled[:,0],X_scaled[:,1],c=y_pred)
# centroids=kmeans.cluster_centers_
# plt.scatter(centroids[:,0],centroids[:,1],c='red',marker='x',s=100,label='聚类中心')
# plt.title('KMeans 无监督聚类结果')
# plt.legend()
# plt.show()
# -----------------------------------------------------------------------------
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.datasets import make_regression
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import r2_score, mean_absolute_error
# x,y=make_regression(
#     n_samples=500,
#     n_features=3,
#     noise=25,
#     random_state=42
# )
# x[:,0]=np.interp(x[:,0],(x[:,0].min(),x[:,0].max()),(50,150))
# x[:,1]=np.interp(x[:,1],(x[:,1].min(),x[:,1].max()),(0,30))
# x[:,2]=np.interp(x[:,2],(x[:,2].min(),x[:,2].max()),(1,5))
# x[:,2]=np.round(x[:,2]).astype(int)
# y=np.interp(y,(y.min(),y.max()),(80,500))
# y=np.round(y,2)
# print('x shape:',x.shape)
# print('y shape:',y.shape)
# print('\n前5行:\n',x[:5])
# print('\n前5个房价:\n',y[:5])
# x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
# model=RandomForestRegressor(n_estimators=100,random_state=42)
# model.fit(x_train,y_train)
# y_pred=model.predict(x_test)
# print('\nR^2:',round(r2_score(y_test,y_pred),4))
# print('\nMAE:',round(mean_absolute_error(y_test,y_pred),2))
# plt.rcParams['font.sans-serif']=['SimHei']
# plt.rcParams['axes.unicode_minus']=False
# plt.figure(figsize=(15, 4))
# #特征分布直方图
# titles=['面积','房龄','房间数']
# for i in range(3):
#     plt.subplot(1,3,i+1)
#     plt.hist(x[:,i],bins=20,color='skyblue',edgecolor='black')
#     plt.title(titles[i])
#     plt.grid(True,alpha=0.3)
# plt.tight_layout()
# plt.show()
# #各特征VS房价散点图
# plt.figure(figsize=(15,4))
# for i in range(3):
#     plt.subplot(1,3,i+1)
#     plt.scatter(x[:,i], y, alpha=0.6, color='orange')
#     plt.xlabel(titles[i])
#     plt.ylabel("房价(万元)")
#     plt.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.show()
# # --- 图3：实际值 vs 预测值 ---
# plt.figure(figsize=(6, 6))
# plt.scatter(y_test, y_pred, alpha=0.7)
# plt.plot([y_test.min(), y_test.max()],
#          [y_test.min(), y_test.max()], 'r--')
# plt.xlabel("实际房价")
# plt.ylabel("预测房价")
# plt.title("实际值 vs 预测值")
# plt.grid(True, alpha=0.3)
# plt.show()
# # --- 图4：特征重要性 ---
# importances = model.feature_importances_
# feat_names = ["面积", "房龄", "房间数"]
# plt.figure(figsize=(6, 4))
# plt.bar(feat_names, importances, color='green')
# plt.title("特征重要性")
# plt.ylabel("重要度")
# plt.show()
# # --- 图5：残差分布 ---
# residuals = y_test - y_pred
# plt.figure(figsize=(6, 4))
# plt.hist(residuals, bins=20, color='purple', alpha=0.7)
# plt.axvline(0, color='red', linestyle='--')
# plt.title("残差分布")
# plt.xlabel("残差")
# plt.show()
#-----------------------------------------
