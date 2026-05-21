#day1
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
#---------------------------------------------------
# m = list(zip('abcd',[66,88,66,77],[88,55,77,88],[66,77,55,88]))
# names = [stu[0] for stu in m]
# k1 = [stu[1] for stu in m]
# k2 = [stu[2] for stu in m]
# k3 = [stu[3] for stu in m]
# def get_max_info(names, fen):
#     max_fen = max(fen)
#     max_index = fen.index(max_fen)
#     max_name = names[max_index]
#     return max_fen, max_name

# max1, name_k1 = get_max_info(names, k1)
# max2, name_k2 = get_max_info(names, k2)
# max3, name_k3 = get_max_info(names, k3)

# for stu in m:
#     name = stu[0]
#     fen = stu[1:]

#     z = (lambda i : sum(i)) (fen)
#     p = (lambda i : sum(i)/len(i)) (fen)

#     if p >85:
#         print(f"学生{name},成绩{fen},总分{z},平均分{p:.2f},优秀")
#     elif p<60:
#         print(f"学生{name},成绩{fen},总分{z},平均分{p:.2f},不及格")
#     else:
#         print(f"学生{name},成绩{fen},总分{z},平均分{p:.2f},合格")
# print(f"第一科最高分：{max1} 分，对应学生：{name_k1}")
# print(f"第二科最高分：{max2} 分，对应学生：{name_k2}")
# print(f"第三科最高分：{max3} 分，对应学生：{name_k3}"
# --------------------------------------------------------------------
# n=float(input())
# if 100>=n>=90:
#     print(f"学生评级为：A")
# elif 90>n>=80:
#     print(f"该学生评级为：B")
# elif 80>n>=70:
#     print(f"该学生评级为：C")
# elif 70>n>=60:
#     print(f"该学生评级为：D")
# elif 60>n>=0:
#     print(f"该学生评级为：E")
# else :
#     print('输入错误请重新输入')
# ------------------------------------------------------------
# sum_score = 0
# count = 0
# while True:
#     try:
#         score = float(input("请输入考试分数："))
#         sum_score += score
#         count += 1
#         while True:
#             m = input("是否继续输入？yes/no：")
#             if m.lower() in ["yes", "no"]:
#                 break
#             print("请输入 yes 或 no！")
#         if m.lower() == "no":
#             break   
#     except ValueError:
#         print("错误：不是一个合法分数，请重新输入！")
#     avg = sum_score / count
# print(f"\n总分数：{sum_score}")
# print(f"平均分：{avg:.2f}")
#--------------------------------------------------------------
# max_p = 0   
# for n in range(2,101):
#     is_prime=True
#     for i in range(2,n):
#         if n%i==0:
#             is_prime=False
#             break
#     if is_prime:
#         print(n,end=' ')
#         max_p = n   
# print("\n100以内最大的质数是：", max_p)
# --------------------------------------------------------------     
# for n in range(1,101):
#     if n%7==0 and n%5!=0:
#         print(n,end=' ')
# --------------------------------------------------------
# for n in range(100,1000):
#     x=n%10
#     y=n//10%10
#     z=n//100
#     if n ==x**3 + y**3+ z**3:
#      print(n)
# ----------------------------------------------
# n=int(input('请输入位数：'))
# start=10**(n - 1)
# end=10**n
# for num in range(start, end):
#     # s = 0
#     # x = num
#     # while x > 0:
#     #         y = x % 10
#     #         s += y ** n
#     #         x = x // 10
#     # if s == num:
#     #         print(num)
#      if sum(map(lambda i : int(i)**n,str(num)))==num:
#        print(num)
# --------------------------------------------------------
# day3
# n=['a','b','c','d']
# n[1] = 'e'
# print(n)
# n.append('f')
# print(n)
# n.insert(1, 'g')
# print(n) 
# n.remove('c')
# print(n)
# last = n.pop(1)
# print(n)
# del n[0]
# print(n) 
# m=['q','p']
# n.extend(m)
# print(n)
# n.sort()#小到大
# print(n)
# n.reverse()#大到小
# print(n)
# u=n.index('f')
# print(u)
# ---------------------------------------------------
# n=[]
# for i in range(3):
#     i=input('请输入三个名字：')
#     n.append(i)
# print(n)    
# n.reverse()
# print(n)
# q=n[1]
# t=n.count(q)
# print(t)
#--------------------------------------------------
# n = ['a','b','c','d']
# m =['1','2','3','4']
# x = dict(zip(n, m))
# print(x)
# print(x['a'])
# print(x.get('b'))
# x['a']=5
# print(x)
# x["e"]=6
# print(x)
# del n['c']
# print(n)
# --------------------------------------
# print('1:更改学生数据')
# print('2:删除学生数据')
# print('3:判断学生男女')
# print('4:查找学生电话')
# print('5:按性别筛选学生')
# o=int(input("请输入选项(1/2/3/4/5)："))
# n={
# 1:{'name':"小红", 'iphone':'123', 'gender':"女"},
# 2:{'name':"小叶", "iphone":'124', 'gender':"男"},
# 3:{"name":"小王", "iphone":'122', 'gender':"男"},
# 4:{'name':"小明", 'iphone':'133', 'gender':"女"}
# }
# for x, y in n.items():
#     print(f"学号：{x}，姓名：{y['name']}，电话：{y['iphone']}，性别：{y['gender']}")
# if o==4:
#     a=int(input(f"输入学生的学号:"))
#     print(n[a]['iphone'])
# elif o==3:
#     num = int(input("请输入学号："))
#     sex = n[num]['gender']
#     if sex == "男":
#         print("该学生是男生")
#     else:
#         print("该学生是女生")
# # n[5]= {'name':'小坚','iphone':'234', 'gender':"男'"}
# # for x,y in n.items():
# #     print(f"学号：{x}，姓名：{y['name']}，电话：{y['iphone']}，性别：{y['gender']}")
# # del n[1]
# # for x,y in n.items():
# #     print(f"学号：{x}，姓名：{y['name']}，电话：{y['iphone']}，性别：{y['gender']}")
# # n.clear()
# # print(n)
# elif o==2:
#     u=int(input("输入需要删除的学号"))
#     n.pop(u)
#     for x,y in n.items():
#        print(f"学号：{x}，姓名：{y['name']}，电话：{y['iphone']}，性别：{y['gender']}")
# # n.popitem()#删最后一行
# # print(n)
# elif o==5:
#     a = input("请输入性别（男/女）：")
#     if a == "男":
#         for x, student in n.items():
#             if student['gender'] == "男":
#                 print(f"学号：{x}，姓名：{student['name']}，电话：{student['iphone']},性别：{student['gender']}")
#     elif a == "女":
#         for x, student in n.items():
#             if student['gender'] == "女":
#                 print(f"学号：{x}，姓名：{student['name']}，电话；{student['iphone']},性别：{student['gender']}")
#     else:
#         print('必须输入的是男或女')
# elif o==1:
#     sid = int(input("输入学号："))
#     n[sid]['iphone'] = input("新电话：")
#     for x,y in n.items():
#         print(f"学号：{x}，姓名：{y['name']}，电话：{y['iphone']}，性别：{y['gender']}")
# else:
#     print("输入无效，请输入1-5")
#----------------------------------------------------------------------
# def demo(newitem,old_list=[]):
#     old_list.append(newitem)
#     return old_list
# print(demo('5',[1,2,3,4]))
# print(demo('aaa',['a','b']))
# print(demo('a'))
# print(demo('b'))
#----------------------------------------------------------------------------
#day4
# n='abcdfab'
# print(n.find('a',4))
# print(n.rfind('a'))
# print(n.index('ab'))
# print(n.rindex('ab'))
# print(n.count('a'))#次数
#----------------------------------------------------------
# text='123456东边来了个小朋友,手里有个小葱123'
# # for index, ch in enumerate(text):
# #     if index == text.index(ch):
# #         print((index,ch),end='')
# # for index, ch in enumerate(text):
# #      times=text.count(ch) 
# #      print(f'下标：{index},字符：{ch}, 次数：{times}')
# print(text.split('个'))
# print(text.rsplit('个'))
# print(text.partition('个小'))
# print(text.rpartition('个小'))
# -------------------------------------------------
# n=('1','2','3')
# m='123qwe'
# for x in n:
#  if x in m:
#      m = m.replace(x,'6')
# print(m)
# table =''.maketrans('abcdef','123456')
# n='aocd3ewsasf3'
# print(n.translate(table))
#----------------------------------------------------
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
#-------------------------------------------------------------
#n='aabbccddeeeffg'
#m=n.strip('af')
#m=n.strip('gaf')
#m=n.strip('gaef')
#m=n.strip('bgaef')
#m=n.strip('gbaefcd')
#print(m)
#---------------------------------------------------------------
# text='''名字:张三 
# 年龄:39 
# 性别:男
# 职业  学生 
# 籍贯:   地球'''
# n=text.split('\n')
# print(n)
# for i in n:
#     print(i[:2],i[2:].strip(':  '),sep=': ',end='\n')
#----------------------------------------------------------
# import string
# print(string.digits)
# print(string.ascii_letters)
#---------------------------------------
# import string
# n=string.ascii_letters + string.digits
# import random
# a=''.join([random.choice(string.punctuation)])
# b=''.join([random.choice(n) for i in range(8)])
# print(a+b)
# --------------------------------------------
# s='hello world\n文本文件的读取方法\n文本文件的写入方法\n'
# with open('sample.text','w') as fp:
#     fp.write(s)
# with open('sample.text') as fp:
#     print(fp.read())
# with open('sample.text','r') as f:
#     s=f.read(5)
# print('s=',s)
# print('字符串s的长度=',len(s))
# with open ('sample.text') as fp:
#     for line in fp:
#         print(line,end='')
# ------------------------------------------------------
# data='9\n8\n7\n6\n5\n4\n3\n2\n1\n0\n'
# with open('data.txt','w') as f:
#     f.write(data)
# with open('data.txt') as f:
#     print(f.read())
# with open('data.txt','r') as fp:
#     lines = []
#     for line in fp:
#         s = line.strip()
#         if s:
#             lines.append(s)
#         n = sorted(lines)
#     data_new='\n'.join(n) 
# with open('data_new.txt','w') as fh:
#     fh.write(data_new)
# print(data_new)
# #-------------------------------------------------
# import os
# n=os.getcwd()
# m=os.listdir(n)
# for i in m:
#      if i.endswith('.py') and os.path.isfile:
#        print(i)
# ----------------------------------------------------
# import os
# n=os.getcwd()
# for root, dirs,files in os.walk(n):
#     print(root)
#     print(dirs)
#     print(files)
# for f in files:
#     print(os.path.join(root,f))
#----------------------------------------------------
#day5
# import os
# n=os.getcwd()
# totalsize=0
# filenum=0
# dirnum=0
# for root, dirs, files in os.walk(n):
#     filenum += len(files)
#     dirnum += len(dirs)
# for f in files:
#         m = os.path.join(root, f)
#         totalsize += os.path.getsize(m)
#         m=int(totalsize)/1024
# print(f"{m:.2f}kb")
# print(filenum)
# print(dirnum)
# -------------------------------------------------
# class shortInputException(Exception):
#     def __init__(self, length,atleast):
#         Exception.__init__(self)
#         self.length= length
#         self.atleast=atleast
# try:
#     s=input('请输入--->')
#     if len(s)<3:
#         raise  shortInputException(len(s),3)
# except EOFError:
#     print('你输入了一个结束标记EOF')
# except shortInputException as x:
#     print('shortInputException :长度是%d,至少应该是%d'%(x.length,x.atleast))
# else:
#  print('没有异常发生')
 #------------------------------------------------------
# while True:
#     x = input('Please input:')
#     try:
#         x = int(x)
#         print(x)
#         print('you have input:{0}'.format(x))
#         break
#     except Exception as e:
#         print('Error.')
#---------------------------------------------------------
# with open ('data.txt') as f:
#     for line in f :
#         print(line,end='')
# #-------------------------------------------------------
while True:
    try:
        n = input("请输入学生成绩：")
        if  n=='':
            raise ValueError("输入不能为空")
        score = float(n)
        if not (0 <= score <= 100):
            raise ValueError("成绩必须在0-100之间")
    except ValueError as e:
        print(f"输入不合法：{e}")
    else:
        print(f"学生的成绩是：{score}")
        break
