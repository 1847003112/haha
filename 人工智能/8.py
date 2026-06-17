import pandas as pd
# student_data={
#     '姓名':['小明','小明','小红','小红'],
#     "科目":["数学","英语","数学",'英语'],
#     "成绩":["90","85","95",'90']
# }
# student_grades=pd.DataFrame(student_data)
# print(student_grades)

# print(student_grades)
# print(student_grades.head())
# print(student_grades.shape[0])
# print(student_grades.info())
# print(student_grades.describe())
# names=student_grades['姓名']
# print('单列姓名：' )
# print(names)

# 读取数据
student_grades = pd.read_csv(r'人工智能\student_scores.csv')

# 查看原始缺失情况
# print("========== 缺失值统计（填充前） ==========")
# print(student_grades.isnull().sum())

# # 处理重复行（完全相同的记录）
# before_dedup = len(student_grades)
# student_grades.drop_duplicates(inplace=True)
# after_dedup = len(student_grades)
# print(f"\n去除完全重复行：{before_dedup} → {after_dedup} 行")

# # 按科目分组，用各科平均分填充该科缺失的成绩
# # transform 保证返回与原始DataFrame长度相同的序列
# student_grades['成绩'] = student_grades['成绩'].fillna(
#     student_grades.groupby('科目')['成绩'].transform('mean')
# )

# # 如果某科目所有成绩都缺失（极端情况），上一步可能仍为NaN，此时可用全局均值兜底
# global_mean = student_grades['成绩'].mean()
# student_grades['成绩'].fillna(global_mean, inplace=True)

# # 查看处理后的结果
# print("\n========== 缺失值统计（填充后） ==========")
# print(student_grades.isnull().sum())

# print("\n========== 处理后的数据 ==========")
# print(student_grades)
subject_avg=student_grades.groupby('科目')['成绩'].mean()
print(subject_avg)
class_gender_max = student_grades.groupby(['班级', '性别'])['成绩'].max()
print(class_gender_max)
