#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
文本情感分类项目：使用Keras实现词嵌入+LSTM/CNN
数据集：IMDB电影评论（二分类：正面/负面）
环境要求：tensorflow, numpy, matplotlib
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

# ========== 设置中文字体，确保图表正常显示中文 ==========
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False   # 解决负号显示异常

# ------------------------------
# 1. 加载与预处理数据
# ------------------------------
max_features = 10000   # 词汇表大小（保留最常见的10000个词）
maxlen = 200           # 评论截断或填充长度

print("正在加载IMDB数据集...")
(x_train, y_train), (x_test, y_test) = keras.datasets.imdb.load_data(num_words=max_features)
print(f"训练集样本数: {len(x_train)}")
print(f"测试集样本数: {len(x_test)}")

# 将不等长的整数序列填充为固定长度
x_train = keras.preprocessing.sequence.pad_sequences(x_train, maxlen=maxlen)
x_test = keras.preprocessing.sequence.pad_sequences(x_test, maxlen=maxlen)
print(f"x_train形状: {x_train.shape}")

# ------------------------------
# 2. 构建LSTM模型
# ------------------------------
def build_lstm_model():
    model = keras.Sequential([
        # 嵌入层：将词索引映射为128维向量
        layers.Embedding(input_dim=max_features, output_dim=128, input_length=maxlen),
        # LSTM层，dropout用于防止过拟合
        layers.LSTM(64, dropout=0.2, recurrent_dropout=0.2),
        # 输出层：二分类使用sigmoid激活
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

lstm_model = build_lstm_model()
print("\nLSTM模型结构：")
lstm_model.summary()

# ------------------------------
# 3. 构建CNN模型
# ------------------------------
def build_cnn_model():
    model = keras.Sequential([
        layers.Embedding(max_features, 128, input_length=maxlen),
        # 一维卷积，kernel_size=5 提取5-gram特征
        layers.Conv1D(128, 5, activation='relu'),
        # 全局最大池化：对每个特征图取最大值
        layers.GlobalMaxPooling1D(),
        # 全连接层
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

cnn_model = build_cnn_model()
print("\nCNN模型结构：")
cnn_model.summary()

# ------------------------------
# 4. 训练模型
# ------------------------------
epochs = 5
batch_size = 32

print("\n开始训练LSTM模型...")
history_lstm = lstm_model.fit(
    x_train, y_train,
    batch_size=batch_size,
    epochs=epochs,
    validation_split=0.2,   # 从训练集中分20%作为验证集
    verbose=1
)

print("\n开始训练CNN模型...")
history_cnn = cnn_model.fit(
    x_train, y_train,
    batch_size=batch_size,
    epochs=epochs,
    validation_split=0.2,
    verbose=1
)

# ------------------------------
# 5. 模型评估与中文图表
# ------------------------------
loss_lstm, acc_lstm = lstm_model.evaluate(x_test, y_test, verbose=0)
loss_cnn, acc_cnn = cnn_model.evaluate(x_test, y_test, verbose=0)
print(f"\nLSTM 测试准确率: {acc_lstm:.4f}  |  CNN 测试准确率: {acc_cnn:.4f}")

def plot_history(history, title):
    """绘制训练与验证的准确率和损失曲线，全部使用中文标签"""
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='训练准确率')
    plt.plot(history.history['val_accuracy'], label='验证准确率')
    plt.title(f'{title} - 准确率')
    plt.xlabel('训练轮次')
    plt.ylabel('准确率')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='训练损失')
    plt.plot(history.history['val_loss'], label='验证损失')
    plt.title(f'{title} - 损失')
    plt.xlabel('训练轮次')
    plt.ylabel('损失值')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

plot_history(history_lstm, 'LSTM')
plot_history(history_cnn, 'CNN')

# ------------------------------
# 6. 对新评论进行预测
# ------------------------------
# 获取词索引映射（将整数还原为词语）
word_index = keras.datasets.imdb.get_word_index()
# 前三个索引保留：0（填充），1（起始），2（未知词）
reverse_word_index = {value + 3: key for key, value in word_index.items()}
reverse_word_index[0] = '<PAD>'
reverse_word_index[1] = '<START>'
reverse_word_index[2] = '<UNK>'

def encode_review(text):
    """将原始文本转换为模型可接受的输入张量"""
    words = text.lower().split()
    seq = []
    for w in words:
        # 未知词映射为索引2，所有索引需偏移3（因为0-2被保留）
        idx = word_index.get(w, 2) + 3
        if idx < max_features:  # 忽略超出词汇表的词
            seq.append(idx)
    padded = keras.preprocessing.sequence.pad_sequences([seq], maxlen=maxlen)
    return padded

# 示例预测
sample_text = "富乐鸡，在五指山路上，交通很是便利。比较鸡肋的是豆芽没有去掉根须，整个菜就显得很掉价，豆腐干有种酸臭味，这个菜等于浪费了。"
encoded_input = encode_review(sample_text)
pred_prob = lstm_model.predict(encoded_input, verbose=0)[0][0]
sentiment = '正面' if pred_prob > 0.5 else '负面'
print(f"\n预测示例:")
print(f"评论: \"{sample_text}\"")
print(f"正面概率: {pred_prob:.4f}  ->  情感判定: {sentiment}")

# 也可用CNN预测
pred_prob_cnn = cnn_model.predict(encoded_input, verbose=0)[0][0]
sentiment_cnn = '正面' if pred_prob_cnn > 0.5 else '负面'
print(f"CNN模型判定: {sentiment_cnn} (概率: {pred_prob_cnn:.4f})")