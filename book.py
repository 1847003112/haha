import pymysql
import time

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

    def add_book(self, book_id, book_name, author, category, state="可借阅"):
        # 给 state 设置默认值，无需用户输入
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
            self.cursor.execute(sql, (book_id,))
            self.conn.commit()
            print("图书删除成功")
            self.write_log(f"删除图书：编号[{book_id}] 书名《{book['book_name']}》")
        except Exception as e:
            self.conn.rollback()
            print("删除失败")

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

# ======================== 主程序 ========================
def main():
    bm = BookManager()
    if not bm.conn:
         return

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
            book_id = input("图书编号：")
            book_name = input("书名：")
            author = input("作者：")
            category = input("分类：")
            # 去掉状态输入，直接调用方法
            bm.add_book(book_id, book_name, author, category)

        elif choice == "2":
            bm.show_all_book()

        elif choice == "3":
            book_id = input("图书编号：")
            bm.search_book_by_id(book_id)

        elif choice == "4":
            book_id = input("要修改的图书编号：")
            new_name = input("新书名：")
            new_author = input("新作者：")
            new_category = input("新分类：")
            bm.update_book(book_id, new_name, new_author, new_category)

        elif choice == "5":
            book_id = input("要删除的图书编号：")
            bm.delete_book(book_id)

        elif choice == "6":
            book_id = input("要借阅的图书编号：")
            bm.borrow_book(book_id)

        elif choice == "7":
            book_id = input("要归还的图书编号：")
            bm.return_book(book_id)

        elif choice == "0":
            bm.close()
            print("👋 系统已退出")
            break

if __name__ == "__main__":
    main()