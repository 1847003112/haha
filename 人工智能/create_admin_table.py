import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='book_db',
    charset='utf8mb4'
)
cursor = conn.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS administer (user_name VARCHAR(50) PRIMARY KEY, password VARCHAR(50))')
cursor.execute("INSERT IGNORE INTO administer (user_name, password) VALUES ('12', '123456')")
conn.commit()
print('Table created and admin user added')
conn.close()