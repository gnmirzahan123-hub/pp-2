import psycopg2

conn=psycopg2.connect(dbname="123",user="postgres",password="mns2007Nur123",host="127.0.0.1",port="5432")
with conn:
    with conn.cursor() as cursor:
        print("connection established")
print(cursor.closed)
conn.close()