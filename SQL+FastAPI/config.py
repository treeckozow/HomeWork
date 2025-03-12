db_username = "treeckozow"
db_password = "treeckozow"
db_hostname = "my_postgres_container"
db_name = "college"
db_table_name = "students"
db_port = "5432"
db_uri = f"postgresql+asyncpg://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_name}"
# postgresql://treeckozow:treeckozow@my_postgres_container:5432/college