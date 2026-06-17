# class Student:
#     school='新余学院'
#     def study(self):
#         print(f"{self.name}正在学习")
# student1=Student()
# student2=Student()
# student1.name,student2.name="a",'b'
# print(student1.school)
# student1.study()
# class Student:
#     def set_name(self,name):
#         self.name=name
#     def get_name(self):
#         return self.name
# s=Student()
# s.set_name('李四')
# print(s.get_name())
#----------------------------------------------
# class Car:
#     color="白色"
#     def run(self):
#         print(f'一辆的{self.color}车正在行驶')
# car1=Car()
# car2=Car()
# car2.color="红色"
# car1.run()
# car2.run()
# ---------------------------------------------------
# class Student:
#     school='新余学院'
#     room='一班'
#     def __init__(self,name,sex='男'):
#         self.name=name
#         self.sex=sex
# s1=Student('张三',)
# s2=Student('李四','女')
# print(s1.name,s1.sex)
# print(s2.name,s2.sex)
# print(s1.school)
# print(s2.room)
# print(Student.school)
# Student.school='江西理工大学'
# print(s1.school,s2.school)
# ------------------------------------------------------
# class Rectangle:
#     def __init__(self,width,height):
#         self.width=width
#         self.height=height
#     def get_area(self):
#         return self.width*self.height    
#     def get_perimeter(self):
#         return (self.width+self.height)*2
#     @classmethod
#     def create_square(cls,side):
#         return cls(side,side)
# n = Rectangle(5, 3)
# print(f"矩形面积：{n.get_area()}")
# print(f"矩形周长：{n.get_perimeter()}")

# m = Rectangle.create_square(4)
# print(f"正方形面积:{m.get_area()}")
# print(f"正方形周长:{m.get_perimeter()}")
# --------------------------------------------------
# class Ferson:
#     def __init__(self,name,age):
#         self.name=name
#         self.__age=age
#     def get_age(self):
#         return self.__age
#     def set_age(self,age):
#         if 0<age<150:self.___age=age
#         else:print('年龄不合格！')
# p=Ferson('张三',20)
# print(p.name)        
# print(p.get_age())
#---------------------------------------------------
# class Shape:
#     def get_area(self):
#         return 0
# class Square(Shape):
#     def __init__(self, side):
#         self.side = side
#     def get_area(self):
#         return self.side ** 2
# class Circle:
#     def __init__(self,radius):
#         self.radius=radius
#     def get_area(self):
#         return self.radius**2*3.14
# def calculate_total_area(shape_list):
#     total = 0
#     for shape in shape_list:
#         total += shape.get_area()
#     return total
# square=Square(4)
# circle=Circle(2)
# total_area = calculate_total_area([square,circle])
# print(f"总面积 = {total_area:.2f}")
#------------------------------------------------------
class BankAccount:
    def __init__(self, account_id, name, balance, password):
        self.account_id = account_id
        self.name = name
        self.__balance = balance
        self.__password = password

    def show_balance(self, input_password):
        if input_password != self.__password:
            print('密码错误！')
        else:
            print(f'当前余额：{self.__balance} 元')

    def deposit(self, money):
        self.__balance += money
        print(f'存入 {money} 元成功，余额：{self.__balance} 元')

    def withdraw(self, input_password, money):
        if input_password != self.__password:
            print('密码错误！')
            return
        if money > self.__balance:
            print('余额不足！')
            return
        self.__balance -= money
        print(f'取款 {money} 元成功，余额：{self.__balance} 元')

    def change_password(self, old_pwd, new_pwd):
        if old_pwd != self.__password:
            print('原密码错误！')
            return
        self.__password = new_pwd
        print('密码修改成功！')
    def lix(self):
        a = int(input("请输入密码查看利息: "))
        if a == self.__password:
            c=int(input('请输入查看年份：'))
            for i in range(c):
             self.__balance=self.__balance+self.__balance*0.015*i
             print(f'第{c}年余额:{self.__balance}')
        else:
            print('密码错误')
            return None
if __name__ == "__main__":
    print("===== 银行账户开户 =====")
    acc_id = input("请输入账号：")
    name = input("请输入姓名：")
    money = int(input("请输入初始金额："))
    pwd = input("请设置密码：")
    my_account = BankAccount(acc_id, name, money, pwd)
    print("\n===== 开户成功！=====")
    p = input("\n请输入密码查看余额：")
    my_account.show_balance(p)
    s = int(input("\n请输入存款金额："))
    my_account.deposit(s)
    p2 = input("\n请输入密码取款：")
    w = int(input("请输入取款金额："))
    my_account.withdraw(p2, w)
    old = input("\n请输入原密码：")
    new = input("请输入新密码：")
    my_account.change_password(old, new)
     