from pydantic import BaseModel
import config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
import sqlalchemy

class StudentInput(BaseModel):
    name: str
    age: int
    email: str

class Student(BaseModel):
    id: int
    name: str
    age: int
    email: str

class StudentManager:
    def __init__(self):
        self.engine: AsyncEngine = create_async_engine(config.db_uri)
        self.students = {}
        self.current_id = 1

    async def getAllStudents(self) -> list[Student]:
        my_query = sqlalchemy.text(f"""
        SELECT * FROM {config.db_table_name}""")
        async with self.engine.connect() as connection:
            result = await connection.execute(my_query)
            rows = result.fetchall()
        return [Student(id=row[0], name=row[1], age=row[2], email=row[3]) for row in rows]
    
    async def getStudentById(self, student_id: int) -> Student:
        my_query = sqlalchemy.text(f'''
        SELECT * FROM {config.db_table_name}
        WHERE id = :id''')
        async with self.engine.begin() as connection:
            result = await connection.execute(
            my_query,
            {"id": student_id}
            )
            row = result.fetchone()
        if row is None:
            return {"Message": "Error, student not found"}
        student = Student(id=row[0], name=row[1], age=row[2], email=row[3])
        return {"Student": student}

    async def addStudent(self, student: StudentInput) -> Student:
        my_query = sqlalchemy.text(f"""
        INSERT INTO {config.db_table_name} (name, age, email) VALUES
        (:name, :age, :email)
        RETURNING row_to_json({config.db_table_name}.*)""")
        async with self.engine.begin() as connection:
            result = await connection.execute(
            (my_query),
            {"name": student.name, "age": student.age, "email": student.email}
            )
            row = result.fetchone()
        return row[0]
    
    async def updateStudent(self, student_id: int, updated_student: StudentInput) -> Student:
        my_query = sqlalchemy.text(f"""
        UPDATE {config.db_table_name}
        SET name = :name, age = :age, email = :email
        WHERE id = :id
        RETURNING row_to_json({config.db_table_name}.*)""")
        async with self.engine.begin() as connection:
            result = await connection.execute(
            my_query,
            {"name": updated_student.name, "age": updated_student.age, "email": updated_student.email, "id": student_id}
            )
            row = result.fetchone()
        if row == None:
            raise KeyError
        return row[0]

        
    async def deleteStudent(self, student_id: int) -> None:
        my_query = sqlalchemy.text(f'''
        DELETE FROM {config.db_table_name} WHERE id = :id''')
        async with self.engine.begin() as connection:
            result = await connection.execute(
            my_query,
            {"id": student_id}
            )
            rows_deleted = result.rowcount
        if rows_deleted == 0:
            raise Exception