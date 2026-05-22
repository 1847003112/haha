import pymysql
import time
<<<<<<< HEAD

=======
from datetime import datetime, timedelta
>>>>>>> feature/update
class BookManager:
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host="localhost",
                user="root",
                password="123456",
                database="book_db",
                charset="utf8mb4"
            )
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            print("[OK] 数据库连接成功")
        except Exception as e:
            print("[ERROR] 数据库连接失败：", e)

    def write_log(self, msg):
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        with open("book_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{now}] {msg}\n")
            
    def admin_login_from_db(self, username, password):
        sql = "SELECT * FROM administer WHERE user_name=%s AND password=%s"
        self.cursor.execute(sql, (username, password))
        res = self.cursor.fetchone()
        return res is not None
<<<<<<< HEAD

    def add_book(self, book_id, book_name, author, category, state="可借阅"):
        # 给 state 设置默认值，无需用户输入
=======
    
    def student_login_from_db(self, student_id, student_password):
        sql = "SELECT * FROM student WHERE student_id=%s AND student_password=%s"
        self.cursor.execute(sql, (student_id, student_password))
        res = self.cursor.fetchone()
        return res is not None
    
    def register_student(self, student_id, student_password):
        """
        学生注册，学号不能重复。
        返回 (成功标志, 提示信息)
        """
        check_sql = "SELECT student_id FROM student WHERE student_id=%s"
        self.cursor.execute(check_sql, (student_id,))
        if self.cursor.fetchone():
            return False, "该学号已被注册，请更换学号"
        
        try:
            insert_sql = "INSERT INTO student (student_id, student_password) VALUES (%s, %s)"
            self.cursor.execute(insert_sql, (student_id, student_password))
            self.conn.commit()
            self.write_log(f"新学生注册：学号[{student_id}]")
            return True, "注册成功，请登录"
        except Exception as e:
            self.conn.rollback()
            return False, f"注册失败：{e}"

    def add_book(self, book_id, book_name, author, category, state="可借阅"):
>>>>>>> feature/update
        try:
            sql = "INSERT INTO book(book_id, book_name, author, category, state) VALUES(%s,%s,%s,%s,%s)"
            self.cursor.execute(sql, (book_id, book_name, author, category, state))
            self.conn.commit()
            print("图书添加成功")
            self.write_log(f"新增图书：编号[{book_id}] 书名《{book_name}》")
        except Exception as e:
            self.conn.rollback()
            print("添加失败！图书编号重复或数据格式错误")

    def show_all_book(self):
        sql = "SELECT * FROM book ORDER BY book_id"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        if not res:
            print("暂无图书数据！")
<<<<<<< HEAD
            return  # 这里修复缩进

        print("\n======================  所有图书列表 ======================")
        # 一本书一行，整洁对齐
        for book in res:
            print(f"编号：{book['book_id']} | 书名：{book['book_name']} | 作者：{book['author']} | 分类：{book['category']} | 状态：{book['state']}")
        print("================================================================")
        

    def search_book_by_id(self, book_id):
        sql = "SELECT * FROM book WHERE book_id = %s"
        self.cursor.execute(sql, (book_id,))
        book = self.cursor.fetchone()
=======
            return
        print("\n======================  所有图书列表 ======================")
        for book in res:
            print(f"编号：{book['book_id']} | 书名：{book['book_name']} | 作者：{book['author']} | 分类：{book['category']} | 状态：{book['state']}")
        print("================================================================")

    def search_book_by_id(self, book_id):
        sql = "SELECT * FROM book WHERE book_id = %s"
        self.cursor.execute(sql, (book_id))
        book = self.cursor.fetchone()

>>>>>>> feature/update
        if book:
            print("\n======================  图书详情 ======================")
            print(f"图书编号：{book['book_id']}")
            print(f"书    名：《{book['book_name']}》")
            print(f"作    者：{book['author']}")
            print(f"分    类：{book['category']}")
            print(f"状    态：{book['state']}")
            print("=" * 55)
        else:
            print("未查询到该图书信息！")
<<<<<<< HEAD
=======
    def search_book_by_name_like(self, keyword):
        sql = "SELECT * FROM book WHERE book_name LIKE %s"
        self.cursor.execute(sql, (f"%{keyword}%",))
        res = self.cursor.fetchall()
        if not res:
            print(f"未找到包含【{keyword}】的图书")
            return
        
        print(f"\n======================  书名模糊查询结果 ======================")
        for book in res:
            print(f"编号：{book['book_id']} | 书名：{book['book_name']} | 作者：{book['author']} | 分类：{book['category']} | 状态：{book['state']}")

    def search_book_by_category(self, category):
        sql = "SELECT * FROM book WHERE category = %s"
        self.cursor.execute(sql, (category,))
        res = self.cursor.fetchall()
        if not res:
            print(f"分类【{category}】暂无图书")
            return
        
        print(f"\n======================  分类【{category}】图书 ======================")
        for book in res:
            print(f"编号：{book['book_id']} | 书名：{book['book_name']} | 作者：{book['author']} | 状态：{book['state']}")

    def search_book_by_author(self, author):
        sql = "SELECT * FROM book WHERE author = %s"
        self.cursor.execute(sql, (author,))
        res = self.cursor.fetchall()
        if not res:
            print(f"作者【{author}】暂无图书")
            return
        
        print(f"\n======================  作者【{author}】图书 ======================")
        for book in res:
            print(f"编号：{book['book_id']} | 书名：{book['book_name']} | 分类：{book['category']} | 状态：{book['state']}")

>>>>>>> feature/update

    def update_book(self, book_id, new_name, new_author, new_category):
        try:
            sql = "UPDATE book SET book_name=%s, author=%s, category=%s WHERE book_id=%s"
            self.cursor.execute(sql, (new_name, new_author, new_category, book_id))
            self.conn.commit()
            print("图书信息修改成功") if self.cursor.rowcount > 0 else print("未找到该图书")
        except Exception as e:
            self.conn.rollback()
            print("修改失败")

    def delete_book(self, book_id):
        sql_check = "SELECT * FROM book WHERE book_id = %s"
        self.cursor.execute(sql_check, (book_id,))
        book = self.cursor.fetchone()
        if not book:
            print("该图书不存在")
            return

        confirm = input(f"确定要删除 编号[{book_id}]《{book['book_name']}》 吗？(y/n)：")
        if confirm.lower() != 'y':
            print("已取消删除")
            return

        try:
            sql = "DELETE FROM book WHERE book_id=%s"
<<<<<<< HEAD
            self.cursor.execute(sql, (book_id,))
=======
            self.cursor.execute(sql, (book_id))
>>>>>>> feature/update
            self.conn.commit()
            print("图书删除成功")
            self.write_log(f"删除图书：编号[{book_id}] 书名《{book['book_name']}》")
        except Exception as e:
            self.conn.rollback()
            print("删除失败")

<<<<<<< HEAD
    def borrow_book(self, book_id):
        sql = "SELECT state FROM book WHERE book_id = %s"
        self.cursor.execute(sql, (book_id,))
        book = self.cursor.fetchone()
        if not book:
            print("不存在该图书")
            return
        if book["state"] == "可借阅":
            update_sql = "UPDATE book SET state='已借出' WHERE book_id=%s"
            self.cursor.execute(update_sql, (book_id,))
            self.conn.commit()
            print("借阅成功")
            self.write_log(f"借阅图书：编号{book_id}")
        else:
            print("该书已借出或状态异常")

    def return_book(self, book_id):
        sql = "SELECT state FROM book WHERE book_id = %s"
        self.cursor.execute(sql, (book_id,))
        book = self.cursor.fetchone()
        if not book:
            print("不存在该图书")
            return
        if book["state"] == "已借出":
            update_sql = "UPDATE book SET state='可借阅' WHERE book_id=%s"
            self.cursor.execute(update_sql, (book_id,))
            self.conn.commit()
            print("归还成功")
            self.write_log(f"归还图书：编号{book_id}")
        else:
            print("该书未被借出")

    def close(self):
        self.cursor.close()
        self.conn.close()

=======
    def borrow_book(self, book_id, student_id):
        # 1. 查询图书状态和名称
        sql = "SELECT state, book_name FROM book WHERE book_id = %s"
        self.cursor.execute(sql, (book_id,))
        book = self.cursor.fetchone()
    
        if not book:
            print("不存在该图书")
            return
    
        if book["state"] != "可借阅":
            print("该图书不可借阅")
            return
    
        # 2. 计算日期
        today = datetime.now().date()
        due_date = today + timedelta(days=7)
        borrow_str = today.strftime("%Y年%m月%d日")
        due_str = due_date.strftime("%Y年%m月%d日")
    
        # 3. 更新数据库（包括事务控制）
        try:
            update_sql = "UPDATE book SET state='已借出' WHERE book_id=%s"
            self.cursor.execute(update_sql, (book_id,))
            self.conn.commit()
        
            # 4. 打印借阅信息
            print("\n" + "=" * 60)
            print(f"当前用户id为：{student_id}")
            print(f"借阅图书为：《{book['book_name']}》")
            print(f"借阅日期为：{borrow_str}")
            print(f"请于{due_str}前归还")
            print("=" * 60)
        
            # 5. 记录日志（确保 self.write_log 方法已定义）
            self.write_log(f"借阅：学号[{student_id}] 借阅[{book_id}]《{book['book_name']}》 应还日期{due_str}")
        
        except Exception as e:
            self.conn.rollback()
            print("借阅失败：", e)
        
    def return_book(self, book_id):
        try:
            # 查询状态和书名
            sql = "SELECT state, book_name FROM book WHERE book_id = %s"
            self.cursor.execute(sql, (book_id,))
            book = self.cursor.fetchone()
        
            if not book:
                print("不存在该图书")
                return
            if book["state"] != "已借出":
                print(f"图书状态为【{book['state']}】，无法归还")
                return
        
            # 更新状态
            update_sql = "UPDATE book SET state='可借阅' WHERE book_id=%s"
            self.cursor.execute(update_sql, (book_id,))
            self.conn.commit()
        
            print(f"《{book['book_name']}》归还成功")
            self.write_log(f"归还图书：编号{book_id}《{book['book_name']}》")
        
        except Exception as e:
            self.conn.rollback()
            print("归还失败：", e)
        
    def close(self):
        self.cursor.close()
        self.conn.close()
>>>>>>> feature/update
# ======================== 主程序 ========================
def main():
    bm = BookManager()
    if not bm.conn:
         return

<<<<<<< HEAD
    print("\n============ 管理员登录 ============")
    while True:
        username = input("请输入管理员账号：")
        password = input("请输入管理员密码：")
        
        if bm.admin_login_from_db(username, password):
            print("登录成功，进入系统")
            break
        else:
            print("账号或密码错误，请重新输入\n")

    while True:
        print("\n==========  图书管理系统 ==========")
        print("1. 添加图书")
        print("2. 查询所有图书")
        print("3. 按编号查询图书")
        print("4. 修改图书信息")
        print("5. 删除图书")
        print("6. 借阅图书")
        print("7. 归还图书")
        print("0. 退出系统")

        choice = input("请输入功能编号：")

        if choice == "1":
=======
    print("\n============ 登录选择 ============")
    print("1 → 管理员登录")
    print("2 → 学生登录")
    print("3 → 学生注册")          
    role_choice = input("请选择登录身份：")

    login_success = False
    is_admin = False
    student_id = None

    if role_choice == "1":
        print("\n===== 管理员登录 =====")
        while True:
            username = input("管理员账号：")
            password = input("管理员密码：")
            if bm.admin_login_from_db(username, password):
                print(" 管理员登录成功")
                login_success = True
                is_admin = True
                break
            else:
                print(" 账号或密码错误")

    elif role_choice == "2":
        print("\n===== 学生登录 =====")
        while True:
            sid = input("学生账号：")
            student_password = input("学生密码：")
            if bm.student_login_from_db(sid, student_password):
                student_id = sid
                print(" 学生登录成功")
                login_success = True
                is_admin = False
                break
            else:
                print(" 账号或密码错误")

    elif role_choice == "3":
        # ========== 学生注册流程 ==========
        print("\n===== 学生注册 =====")
        while True:
            new_id = input("请输入账号：")
            new_pwd = input("请输入密码：")
            confirm_pwd = input("请再次输入密码：")
            success, msg = bm.register_student(new_id, new_pwd)
            print(msg)
            if success:
                input("按回车键前往登录...")
                print("\n===== 学生登录 =====")
                while True:
                    sid = input("学生账号：")
                    student_password = input("学生密码：")
                    if bm.student_login_from_db(sid, student_password):
                        student_id = sid
                        print(" 学生登录成功")
                        login_success = True
                        is_admin = False
                        break
                    else:
                        print(" 账号或密码错误")
                break
            else:
                retry = input("是否重新注册？(y/n)：")
                if retry.lower() != 'y':
                    print("已取消注册，退出系统")
                    return
    else:
        print("输入错误，退出系统")
        return

    # ===================== 菜单 =====================
    while True:
        print("\n========== 图书管理系统 ==========")
        
        if is_admin:
            print("1 → 添加图书")
            print("2 → 查询所有图书")
            print("3 → 按编号查询图书")
            print("4 → 修改图书信息")
            print("5 → 删除图书")
            print("6 → 借阅图书")
            print("7 → 归还图书")
            print("8 → 按书名模糊查询")    
            print("9 → 按分类筛选")        
            print("10 → 按作者筛选")
            print("0 → 退出系统")
        else:
            print("2 → 查询所有图书")
            print("3 → 按编号查询图书")
            print("6 → 借阅图书")
            print("7 → 归还图书")
            print("8 → 按书名模糊查询")    
            print("9 → 按分类筛选")        
            print("10 → 按作者筛选")
            print("0 → 退出系统")
        choice = input("请输入功能编号：")

        if is_admin and choice == "1":
>>>>>>> feature/update
            book_id = input("图书编号：")
            book_name = input("书名：")
            author = input("作者：")
            category = input("分类：")
<<<<<<< HEAD
            # 去掉状态输入，直接调用方法
=======
>>>>>>> feature/update
            bm.add_book(book_id, book_name, author, category)

        elif choice == "2":
            bm.show_all_book()

        elif choice == "3":
            book_id = input("图书编号：")
            bm.search_book_by_id(book_id)

<<<<<<< HEAD
        elif choice == "4":
=======
        elif is_admin and choice == "4":
>>>>>>> feature/update
            book_id = input("要修改的图书编号：")
            new_name = input("新书名：")
            new_author = input("新作者：")
            new_category = input("新分类：")
            bm.update_book(book_id, new_name, new_author, new_category)

<<<<<<< HEAD
        elif choice == "5":
=======
        elif is_admin and choice == "5":
>>>>>>> feature/update
            book_id = input("要删除的图书编号：")
            bm.delete_book(book_id)

        elif choice == "6":
            book_id = input("要借阅的图书编号：")
<<<<<<< HEAD
            bm.borrow_book(book_id)
=======
            bm.borrow_book(book_id, student_id)
>>>>>>> feature/update

        elif choice == "7":
            book_id = input("要归还的图书编号：")
            bm.return_book(book_id)
<<<<<<< HEAD

        elif choice == "0":
            bm.close()
            print("👋 系统已退出")
            break

=======
        elif choice == "8":
            keyword = input("请输入书名关键词：")
            bm.search_book_by_name_like(keyword)

        elif choice == "9":
            category = input("请输入图书分类：")
            bm.search_book_by_category(category)

        elif choice == "10":
            author = input("请输入作者名称：")
            bm.search_book_by_author(author)
        elif choice == "0":
            bm.close()
            print(" 系统已退出")
            break

        elif not is_admin and choice in ["1","4","5"]:
            print(" 权限不足！学生无法使用此功能")

        else:
            print("输入错误，请重新输入")

>>>>>>> feature/update
if __name__ == "__main__":
    main()