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
            print(f'当前余额：{self.__balance:.2f} 元')
    def deposit(self, money):
        if money <= 0:
            print("存款金额必须大于0！")
            return
        self.__balance += money
        print(f'存入 {money} 元成功，余额：{self.__balance:.2f} 元')
    def withdraw(self, input_password, money):
        if input_password != self.__password:
            print('密码错误！')
            return
        if money <= 0:
            print("取款金额必须大于0！")
            return
        if money > self.__balance:
            print('余额不足！')
            return
        self.__balance -= money
        print(f'取款 {money} 元成功，余额：{self.__balance:.2f} 元')
    def change_password(self, old_pwd, new_pwd):
        if old_pwd != self.__password:
            print('原密码错误！')
            return
        self.__password = new_pwd
        print('密码修改成功！')
    def calculate_interest(self):
        pwd = input("请输入密码查看利息: ")
        if pwd != self.__password:
            print('密码错误')
            return
        original_balance = self.__balance
        try:
            years = int(input('请输入查看年份：'))
            if years <= 0:
                print("年份必须大于0！")
                return
        except ValueError:
            print("请输入有效数字！")
            return
        temp_balance = original_balance
        for year in range(1, years + 1):
            temp_balance = temp_balance * 1.015  # 年复利 1.5%
            print(f'第{year}年余额: {temp_balance:.2f} 元')
        
        print(f"\n原始本金: {original_balance:.2f} 元，{years}年后预计本息: {temp_balance:.2f} 元")

if __name__ == "__main__":
    print("===== 银行账户开户 =====")
    acc_id = input("请输入账号：")
    name = input("请输入姓名：")
    while True:
        try:
            money = int(input("请输入初始金额："))
            if money >= 0:
                break
            else:
                print("初始金额不能为负数！")
        except ValueError:
            print("请输入数字！")   
    pwd = input("请设置密码：")
    my_account = BankAccount(acc_id, name, money, pwd)
    print("\n===== 开户成功！=====")
    p = input("\n请输入密码查看余额：")
    my_account.show_balance(p)

    while True:
        try:
            s = int(input("\n请输入存款金额："))
            my_account.deposit(s)
            break
        except ValueError:
            print("请输入有效数字！")
    p2 = input("\n请输入密码取款：")
    while True:
        try:
            w = int(input("请输入取款金额："))
            my_account.withdraw(p2, w)
            break
        except ValueError:
            print("请输入有效数字！")
    old = input("\n请输入原密码：")
    new = input("请输入新密码：")
    my_account.change_password(old, new)
    print("\n----- 利息计算 -----")
    my_account.calculate_interest()