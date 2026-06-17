# import jieba
# text = '我的小猫在做猫饼了'
# seg_list = jieba.lcut(text, cut_all=False)  # 转为列表，可多次使用
# print('分词结果:', '/'.join(seg_list))
# stopwords = {'的', '了', '在'}  # 用集合提高查找效率
# filtered = [w for w in seg_list if w not in stopwords]
# print(filtered)
# -----------------------------
# import jieba
# text = "我爱自然语言处理"
# seg_list = jieba.cut(text,cut_all = False)
# # print(list(seg_list))

# print("分词结果:"+"|".join(seg_list))
# stopwords = {'的','了','在'}
# filtered = [w for w in['我','爱','自然语言处理'] if w not in stopwords]
import jieba
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
# 导入TF-IDF文本特征提取工具，把文本转换成数字向量
from sklearn.naive_bayes import MultinomialNB
# 多项式朴素贝叶斯分类器，专门用于文本分类的经典机器学习算法
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1 数据集
data_list = [
    # 正面
    ("味道超棒，服务好", 1),
    ("电影太好看了，强烈推荐", 1),
    ("商品质量不错，物流很快", 1),
    ("环境优雅，性价比很高", 1),
    ("非常满意，下次还来", 1),
    ("味道好，干净卫生", 1),
    ("超出预期，体验极佳", 1),
    ("客服态度好，问题解决快", 1),
    ("产品做工精细，细节到位", 1),
    ("价格实惠，物超所值", 1),
    ("服务周到，让人舒服", 1),
    ("效果远超预期，非常满意", 1),
    ("物流快，包装好", 1),
    ("口味正宗，分量十足", 1),
    ("质量上乘，值得购买", 1),
    ("体验感满分，强烈安利", 1),
    ("环境干净整洁，体验很好", 1),
    ("态度热情，全程很愉快", 1),
    ("效果很好，会回购的", 1),
    ("各方面都很满意，好评", 1),
    # 负面
    ("太难吃了，再也不会来这家店", 0),
    ("电影剧情无聊，浪费时间", 0),
    ("商品质量差，发货很慢", 0),
    ("价格贵，体验很差", 0),
    ("非常失望，不推荐购买", 0),
    ("卡顿严重，体验极差", 0),
    ("做工粗糙，不值这个价", 0),
    ("客服态度差，解决不了问题", 0),
    ("物流太慢了，等了半个月", 0),
    ("味道难吃，完全踩雷", 0),
    ("质量堪忧，用了两天就坏了", 0),
    ("价格虚高，完全不值", 0),
    ("服务态度恶劣，再也不来", 0),
    ("效果很差，完全没用", 0),
    ("体验糟糕，差评", 0),
    ("环境脏乱差，太失望了", 0),
    ("态度冷漠，全程很糟心", 0),
    ("发货错误，售后也不管", 0),
    ("质量问题严重，不建议买", 0),
    ("完全不符合预期，避雷", 0)
]

texts = [i[0] for i in data_list]
labels = [i[1] for i in data_list]
df = pd.DataFrame({"text": texts, "label": labels})
# print(df.head())

# 2 自定义停用词
stop_words = {"的", "了", "也", "很", "都", "就", "是", "会", "来", "这", "还会", "再"}

# 3 分词 + 过滤停用词
def cut_and_filter(text):
    words = jieba.lcut(text)
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

df["cut_text"] = df["text"].apply(cut_and_filter)
X = df["cut_text"]
# print(X)
y = df["label"]

# 4 TF-IDF 调参
tfidf = TfidfVectorizer(ngram_range=(1,2)) # 增加二元语法，捕获短语
# ngram_range=(1,2) 表示同时提取一元词（单个词）和二元词（两个连续的词）
# 比如句子“味道超棒”，会拆分出“味道”“超棒”“味道 超棒”
X_tfidf = tfidf.fit_transform(X)
# 把文本数据转换成 TF-IDF 特征矩阵

# 5 划分数据集
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf, y, test_size=0.2, random_state=66, stratify=y
)

# 6 训练模型
clf = MultinomialNB(alpha=0.8) # 平滑系数微调
clf.fit(X_train, y_train)

# 评估
y_pred = clf.predict(X_test)
print(f"测试集准确率：{accuracy_score(y_test, y_pred):.4f}")
#预测函数
def pred_sent(text):
    txt = cut_and_filter(text)
    print(txt)
    vec = tfidf.transform([txt])
    print(vec)
    res = clf.predict(vec)[0]
    return '正面' if res==1 else '负面'
print('\n测试时间:')
print(pred_sent('服务好,还会再来'))
print(pred_sent('服务差,体验糟糕'))                 