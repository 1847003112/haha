# import pymysql

# DB_CONFIG = {
#     'host': 'localhost',
#     'port': 3306,
#     'user': 'root',
#     'password': '123456',
#     'database': 'company1',
#     'charset': 'utf8mb4'
# }

# conn = None
# cursor = None

# try:
#     conn = pymysql.connect(**DB_CONFIG)
#     print("成功连接到 company1 数据库")
    
#     cursor = conn.cursor()

#     # 1. 创建表
#     create_table_sql = """
#         CREATE TABLE IF NOT EXISTS user (
#             id INT PRIMARY KEY AUTO_INCREMENT,
#             username VARCHAR(50) NOT NULL,
#             phone VARCHAR(20),
#             gender enum('男','女') DEFAULT '男'
#         ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
#         """
#     cursor.execute(create_table_sql)
#     print("user 表创建成功")
    
#     # 2. 插入初始化数据
#     tian_sql = """
#     INSERT INTO user (id, username, phone, gender) VALUES 
#     (1, '赵一', '111111', '男'),
#     (2, '钱二', '222222', '女'),
#     (3, '孙三', '333333', '男'),
#     (4, '李四', '444444', '男'),
#     (5, '孔五', '555555', '女')
#     """
#     cursor.execute(tian_sql)
#     conn.commit()
#     print('插入成功')

#     # 查询所有男生
#     def hun1():
#         zhao_sql = "SELECT * FROM user WHERE gender='男'"
#         cursor.execute(zhao_sql)
#         print("所有男生：", cursor.fetchall())

#     # 修改手机号
#     def hun2():
#         cursor.execute("UPDATE user SET phone='123456' WHERE id=1")
#         conn.commit()
#         print("修改成功")

#     # 删除id=3的数据
#     def hun3():
#         cursor.execute("DELETE FROM user WHERE id=3")
#         conn.commit()
#         print("删除成功")

#     # 事务插入
#     def hun4():
#         try:
#             conn.begin()
#             sql_trans1 = "INSERT INTO user (username, phone, gender) VALUES ('周一', '13912345678', '男')"
#             sql_trans2 = "INSERT INTO user (username, phone, gender) VALUES ('林二', '13987654321', '女')"
#             cursor.execute(sql_trans1)
#             cursor.execute(sql_trans2)
#             conn.commit()
#             print("事务提交成功")
#         except pymysql.MySQLError as e:
#             conn.rollback()
#             print(f"操作失败: {e}")

#     # 菜单循环
#     while True:
#         print("\n===== 菜单 =====")
#         print("1 - 查询所有男生")
#         print("2 - 修改id=1的手机号")
#         print("3 - 删除id=3的数据")
#         print("4 - 事务插入两条数据")
#         print("0 - 退出")
        
#         choice = input("请输入数字选择功能：")
        
#         if choice == "1":
#             hun1()
#         elif choice == "2":
#             hun2()
#         elif choice == "3":
#             hun3()
#         elif choice == "4":
#             hun4()
#         elif choice == "0":
#             print("退出程序")
#             break
#         else:
#             print("输入无效，请重新输入")

# except Exception as e:
#     print(f"批量插入失败: {e}")

# finally:
#     if cursor:
#         cursor.close()
#     if conn:
#         conn.close()
#     print("资源已释放")
import pymysql

class DBHelper:
    def __init__(self, host, user, pwd, db, port=3306):
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=pwd,
            database=db,
            port=port,
            charset='utf8mb4'
        )
        self.cursor = self.conn.cursor()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        try:
            self.cursor.execute(sql, params or ())
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print("执行失败：", e)
            return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

class StudentManager:
    def __init__(self, db_helper):
        self.db = db_helper
        self._ensure_address_column()

    def _ensure_address_column(self):
        try:
            self.db.query("SHOW COLUMNS FROM student LIKE 'address'")
            self.db.execute("ALTER TABLE student ADD COLUMN address VARCHAR(100) DEFAULT NULL")
            print("已添加 address 字段")
        except:
            pass

    def add_student(self, name, age, gender, major, address=None):
        sql = """
        INSERT INTO student(name, age, gender, major, address)
        VALUES (%s, %s, %s, %s, %s)
        """
        return self.db.execute(sql, (name, age, gender, major, address))

    def get_student_by_id(self, sid):
        sql = "SELECT * FROM student WHERE id = %s"
        return self.db.query(sql, (sid,))

    def update_address(self, sid, new_address):
        sql = "UPDATE student SET address = %s WHERE id = %s"
        return self.db.execute(sql, (new_address, sid))

    def delete_student(self, sid):
        sql = "DELETE FROM student WHERE id = %s"
        return self.db.execute(sql, (sid,))

def create_student_table(db):
    sql = """
    CREATE TABLE IF NOT EXISTS student (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(30) NOT NULL,
        age INT,
        gender ENUM('男','女') DEFAULT '男',
        major VARCHAR(50)
    )
    """
    db.execute(sql)
    print("student 表创建成功")

if __name__ == '__main__':
    db = DBHelper(
        host="localhost",
        user="root",
        pwd="123456",
        db="company",
        port=3306
    )

    create_student_table(db)
    stu_manager = StudentManager(db)

    stu_manager.add_student("陈小燕", 20, "女", "计算机科学", "北京市海淀区")
    stu_manager.add_student("刘伟", 21, "男", "软件工程", "上海市浦东新区")
    stu_manager.add_student("赵雅", 19, "女", "数据科学", "广州市天河区")
    stu_manager.add_student("黄涛", 22, "男", "人工智能", "深圳市南山区")
    print("4 条学生数据插入成功")

    print("查询 id=2 的学生：")
    print(stu_manager.get_student_by_id(2))

    stu_manager.update_address(3, "四川省成都市高新区")
    print("id=3 地址已更新")

    stu_manager.delete_student(4)
    print("id=4 已删除")

    print("最终所有学生：")
    all_stu = db.query("SELECT * FROM student")
    for s in all_stu:
        print(s)

    db.close()