# print("1,加法")
# print("2,减法")
# print("3,乘法")
# print("4,除法")

# a = input("请输入选项(1/2/3/4)：")
# b = float(input("输入一个数："))
# c = float(input("输入另一个数："))

# if a == "1":
#     n = b + c
#     print(n)
# elif a == "2":
#     n = b - c
#     print(n)
# elif a == "3":
#     n = b * c
#     print(n)
# elif a == "4":
#     if c == 0:
#         print("除数不能为0，请重新输入")
#     else:
#         n = b / c
#         print(n)
# else:
#     print("输入无效，请输入1-4")
# -----------------------------------------
def main():
    print('1:更改学生数据')
    print('2:删除学生数据')
    print('3:判断学生男女')
    print('4:查找学生电话')
    print('5:按性别筛选学生')
    o=int(input("请输入选项(1/2/3/4/5)："))
    n={
    1:{'name':"小红", 'iphone':'123', 'gender':"女"},
    2:{'name':"小叶", "iphone":'124', 'gender':"男"},
    3:{"name":"小王", "iphone":'122', 'gender':"男"},
    4:{'name':"小明", 'iphone':'133', 'gender':"女"}
    }
    for x, y in n.items():
        print(f"学号：{x}，姓名：{y['name']}，电话：{y['iphone']}，性别：{y['gender']}")
    if o==4:
        a=int(input(f"输入学生的学号:"))
        print(n[a]['iphone'])
    elif o==3:
        num = int(input("请输入学号："))
        sex = n[num]['gender']
        if sex == "男":
            print("该学生是男生")
        else:
            print("该学生是女生")
# n[5]= {'name':'小坚','iphone':'234', 'gender':"男'"}
# for x,y in n.items():
#     print(f"学号：{x}，姓名：{y['name']}，电话：{y['iphone']}，性别：{y['gender']}")
# del n[1]
# for x,y in n.items():
#     print(f"学号：{x}，姓名：{y['name']}，电话：{y['iphone']}，性别：{y['gender']}")
# n.clear()
# print(n)
    elif o==2:
        u=int(input("输入需要删除的学号"))
        n.pop(u)
        for x,y in n.items():
            print(f"学号：{x}，姓名：{y['name']}，电话：{y['iphone']}，性别：{y['gender']}")
# n.popitem()#删最后一行
# print(n)
    elif o==5:
        a = input("请输入性别（男/女）：")
        if a == "男":
            for x, student in n.items():
                if student['gender'] == "男":
                    print(f"学号：{x}，姓名：{student['name']}，电话：{student['iphone']},性别：{student['gender']}")
        elif a == "女":
            for x, student in n.items():
                if student['gender'] == "女":
                    print(f"学号：{x}，姓名：{student['name']}，电话；{student['iphone']},性别：{student['gender']}")
        else:
            print('必须输入的是男或女')
    elif o==1:
        sid = int(input("输入学号："))
        n[sid]['iphone'] = input("新电话：")
        for x,y in n.items():
            print(f"学号：{x}，姓名：{y['name']}，电话：{y['iphone']}，性别：{y['gender']}")
    else:
        print("输入无效，请输入1-5")
main()