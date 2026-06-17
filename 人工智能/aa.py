from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Optional,List
import pymysql

app = FastAPI()

def get_db_connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='123456',
        database='student_db',
        charset='utf8mb4',
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

class Student(BaseModel):
    id: int
    name: str
    age: int

@app.get("/students")
def get_all_student():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("select * from students")
    students = cursor.fetchall()
    conn.close()
    return {"data": students}
@app.post("/students/")
def create_student(stu: Student):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO students (id, name, age) VALUES ({stu.id}, '{stu.name}', {stu.age})")
    conn.commit()
    conn.close()            
    return {"data": "创建成功"}

@app.put("/students/{id}")
def update_student(id: int, stu: Student):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE students SET name = '{stu.name}', age = {stu.age} WHERE id = {id}")
    conn.commit()
    conn.close()
    return {"data": "更新成功"}

@app.delete("/students/{id}")
def delete_student(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM students WHERE id = {id}")
    conn.commit()
    conn.close()
    return {"data": "删除成功"}
@app.get("/students/search")
def search_students(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    field: Optional[str] = Query("name", description="搜索字段: name/student_id/class")
):
    # 白名单限制，防止 SQL 注入
    allowed_fields = {"name", "student_id", "class"}
    if field not in allowed_fields:
        field = "name"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = f"SELECT * FROM students WHERE {field} LIKE %s"
    cursor.execute(sql, (f"%{keyword}%",))
    results = cursor.fetchall()
    conn.close()
    
    return {"count": len(results), "students": results}
@app.get("/students/stats")
def get_student_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total, AVG(age) as average_age FROM students")
    result = cursor.fetchone()
    conn.close()
    total = result['total'] 
    avg_age = result['average_age']
    average_age = round(avg_age, 2) 
    
    return {"total": total, "average_age": average_age}
class Student(BaseModel):
    name: str
    age: int
   
@app.post("/students/batch")
def insert_students_batch(students: List[Student]):
    if not students:
        raise HTTPException(status_code=400, detail="学生列表不能为空")
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO students (name, age) VALUES (%s, %s)"
    data = [(s.name, s.age) for s in students]
    cursor.executemany(sql, data)
    conn.commit()
    inserted_count = cursor.rowcount
    last_id = cursor.lastrowid
    conn.close()
    first_id = last_id - inserted_count + 1
    inserted_ids = list(range(first_id, last_id + 1))
    return {
        "inserted_count": inserted_count,
        "inserted_ids": inserted_ids
    }