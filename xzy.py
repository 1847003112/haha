# def get_student_data():
#     return {
#         1: {'name': "小红", 'iphone': '123', 'gender': "女"},
#         2: {'name': "小叶", "iphone": '124', 'gender': "男"},
#         3: {'name': "小王", "iphone": '122', 'gender': "男"},
#         4: {'name': "小明", 'iphone': '133', 'gender': "女"}
#     }
# def print_menu():
#     print("\n===== 学生管理系统 =====")
#     print('1: 更改学生数据')
#     print('2: 删除学生数据')
#     print('3: 判断学生男女')
#     print('4: 查找学生电话')
#     print('5: 按性别筛选学生')
#     print('0: 退出程序')
# def showstu(n):
#     print("\n----- 当前学生列表 -----")
#     for sid, info in n.items():
#         print(f"学号：{sid}，姓名：{info['name']}，电话：{info['iphone']}，性别：{info['gender']}")
#     print("------------------------\n")
# def xiustu(n):
#     try:
#         sid = int(input("输入要修改的学生学号："))
#         if sid not in n:
#             print("该学号不存在！")
#             return
#         n[sid]['iphone'] = input("请输入新电话：")
#         print("修改成功！")
#         showstu(n)
#     except:
#         print("输入格式错误！")
# def delstu(n):
#     try:
#         sid = int(input("输入需要删除的学号："))
#         if sid not in n:
#             print("该学号不存在！")
#             return
#         n.pop(sid)
#         print("删除成功！")
#         showstu(n)
#     except:
#         print("输入格式错误！")
# def zhao(n):
#     try:
#         sid = int(input("请输入学号："))
#         if sid not in n:
#             print("该学号不存在！")
#             return
#         sex = n[sid]['gender']
#         if sex == "男":
#             print("该学生是男生")
#         else:
#             print("该学生是女生")
#     except:
#         print("输入格式错误！")
# def iphone(n):
#     try:
#         sid = int(input("输入学生的学号："))
#         if sid not in n:
#             print("该学号不存在！")
#             return
#         print("学生电话：", n[sid]['iphone'])
#     except:
#         print("输入格式错误！")
# def xuanstu(n):
#     gender = input("请输入性别（男/女）：")
#     if gender not in ["男", "女"]:
#         print('必须输入 男 或 女')
#         return
#     print(f"\n----- {gender}生列表 -----")
#     count = 0
#     for sid, student in n.items():
#         if student['gender'] == gender:
#             print(f"学号：{sid}，姓名：{student['name']}，电话：{student['iphone']}，性别：{student['gender']}")
#             count += 1
#     if count == 0:
#         print(f"没有找到{gender}生")
#     print("------------------------\n")
# def main():
#     students = get_student_data()
#     while True:
#         print_menu()
#         try:
#             choice = int(input("请输入选项(0-5)："))
#         except:
#             print("输入错误，请输入数字！")
#             continue
#         if choice == 0:
#             print("感谢使用，再见！")
#             break
#         showstu(students)
#         if choice == 1:
#             xiustu(students)
#         elif choice == 2:
#             delstu(students)
#         elif choice == 3:
#             zhao(students)
#         elif choice == 4:
#             iphone(students)
#         elif choice == 5:
#             xuanstu(students)
#         else:
#             print("输入无效，请输入 0-5")
# if __name__ == "__main__":
#     main()
#----------------------------------------------------------------------
# test = 'hbaseo world! I like python. this is a nice day. right?'

# def print_menu():
#     print('===== 文本处理程序 =====')
#     print('1: 大小写转换')
#     print('2: 统计每个单词个数')
#     print('3: 字母加密（后移3位）')
#     print('0: 退出程序')
#     print('========================')

# def daxiaoxie():
#     print("\n【大写】：", test.upper())
#     print("【小写】：", test.lower())
#     print()

# def geshu():
#     temp = test
#     n = ('!', '.', '?')
#     for x in n:
#         temp = temp.replace(x, ' ')
#     m = temp.split()
    
#     print("\n【单词列表】：", m)
#     print("【统计结果】：")
#     seen = []
#     for ch in m:
#         if ch not in seen:
#             seen.append(ch)
#             times = m.count(ch)
#             print(f'   单词：{ch}，次数：{times}')
#     print()
# def jiami():
#     lower_letter = 'abcdefghijklmnopqrstuvwxyz'
#     upper_letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
#     k = 3
#     lower_letter_k = lower_letter[k:] + lower_letter[:k]
#     upper_letter_k = upper_letter[k:] + upper_letter[:k]
#     a = lower_letter + upper_letter
#     b = lower_letter_k + upper_letter_k
#     c = test.maketrans(a, b)
#     d = test.translate(c)
#     print("\n【加密结果】：", d)
#     print()
# def main():
#     while True:
#         print_menu()
#         try:
#             choice = int(input("请输入选项(0-3)："))
#         except:
#             print("输入错误，请输入数字！\n")
#             continue
#         if choice == 0:
#             print("感谢使用，再见！")
#             break
#         elif choice == 1:
#             daxiaoxie()
#         elif choice == 2:
#             geshu()
#         elif choice == 3:
#             jiami()
#         else:
#             print("输入无效，请输入 0-3！\n")
# if __name__ == "__main__":
#     main()
#---------------------------------------------------