from pydantic import BaseModel
import config
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
        self.engine = sqlalchemy.create_engine(config.db_uri)
        self.students = {}
        self.current_id = 1

    def getAllStudents(self) -> list[Student]:
        my_query = f"""
        SELECT * FROM {config.db_table_name}"""
        with self.engine.connect() as connection:
            result = connection.execute(
            sqlalchemy.text(my_query)
            )
        return [
            Student(id=row[0], name=row[1], age=row[2], email=row[3])
            for row in result
            ]
    
    def getStudentById(self, student_id: int) -> Student:
        my_query = f'''
        SELECT * FROM {config.db_table_name}
        WHERE id = :id'''
        try:
            with self.engine.connect() as connection:
                transaction = connection.begin()
                result = connection.execute(
                sqlalchemy.text(my_query),
                {"id": student_id}
                )
                row = result.fetchone()
                transaction.commit()
            student = Student(id=row[0], name=row[1], age=row[2], email=row[3])
            return {"Student": student}
        except:
            return {"Message": "Error, student not found"}

    def addStudent(self, student: StudentInput) -> Student:
        my_query = f"""
        INSERT INTO {config.db_table_name} (name, age, email) VALUES
        (:name, :age, :email)
        RETURNING row_to_json({config.db_table_name}.*)"""
        with self.engine.connect() as connection:
            transaction = connection.begin()
            result = connection.execute(
            sqlalchemy.text(my_query),
            {"name": student.name, "age": student.age, "email": student.email}
            )
            row = result.fetchone()
            transaction.commit()
        return row[0]
    
    def updateStudent(self, student_id: int, updated_student: StudentInput) -> Student:
        my_query = f"""
        UPDATE {config.db_table_name}
        SET name = :name, age = :age, email = :email
        WHERE id = :id
        RETURNING row_to_json({config.db_table_name}.*)"""
        with self.engine.connect() as connection:
            transaction = connection.begin()
            result = connection.execute(
            sqlalchemy.text(my_query),
             {"name": updated_student.name, "age": updated_student.age, "email": updated_student.email, "id": student_id}
            )
            transaction.commit()
            row = result.fetchone()
        if row == None:
            raise KeyError
        return row[0]

        
    def deleteStudent(self, student_id: int) -> None:
        my_query = f'''
        DELETE FROM {config.db_table_name} WHERE id = :id'''
        with self.engine.connect() as connection:
            transaction = connection.begin()
            result = connection.execute(
            sqlalchemy.text(my_query),
            {"id": student_id}
            )
            transaction.commit()
            rows_deleted = result.rowcount
        if rows_deleted == 0:
            raise Exception