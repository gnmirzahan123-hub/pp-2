import psycopg2

# подключаемся к базе
conn = psycopg2.connect(
    dbname="123",   # имя вашей базы
    user="postgres",
    password="mns2007Nur123",
    host="127.0.0.1",
    port="5432"
)

cursor = conn.cursor()

# выполняем SQL команду через курсор
cursor.execute("""
    CREATE TABLE people (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        age INTEGER
    )
""")

conn.commit()   # сохраняем изменения
print("Таблица создана!")

cursor.close()
conn.close()
