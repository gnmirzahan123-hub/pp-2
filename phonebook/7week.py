import psycopg2
import csv


def get_connection():
    return psycopg2.connect(
        dbname="1",      # имя вашей базы
        user="postgres",   # ваш пользователь
        password="mns2007Nur123",
        host="127.0.0.1",
        port="5432"
    )


def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            phone VARCHAR(20)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()


def insert_from_csv(filename):
    conn = get_connection()
    cursor = conn.cursor()
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            cursor.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()
    cursor.close()
    conn.close()


def insert_from_console():
    name = input("Введите имя: ")
    phone = input("Введите телефон: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cursor.close()
    conn.close()


def update_contact():
    name = input("Введите имя контакта для обновления: ")
    new_phone = input("Введите новый телефон: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE phonebook SET phone=%s WHERE name=%s", (new_phone, name))
    conn.commit()
    cursor.close()
    conn.close()

def query_contacts():
    choice = input("Искать по (1) имени или (2) префиксу телефона: ")
    conn = get_connection()
    cursor = conn.cursor()
    if choice == "1":
        name = input("Введите имя: ")
        cursor.execute("SELECT * FROM phonebook WHERE name=%s", (name,))
    else:
        prefix = input("Введите префикс телефона: ")
        cursor.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (prefix + "%",))
    print(cursor.fetchall())
    cursor.close()
    conn.close()


def delete_contact():
    choice = input("Удалить по (1) имени или (2) телефону: ")
    conn = get_connection()
    cursor = conn.cursor()
    if choice == "1":
        name = input("Введите имя: ")
        cursor.execute("DELETE FROM phonebook WHERE name=%s", (name,))
    else:
        phone = input("Введите телефон: ")
        cursor.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
    conn.commit()
    cursor.close()
    conn.close()


create_table()
while True:
    print("\n--- PhoneBook Menu ---")
    print("1. Добавить контакт из CSV")
    print("2. Добавить контакт вручную")
    print("3. Обновить контакт")
    print("4. Найти контакт")
    print("5. Удалить контакт")
    print("6. Выйти")
    choice = input("Выберите действие: ")
    if choice == "1":
        insert_from_csv("contacts.csv")
    elif choice == "2":
        insert_from_console()
    elif choice == "3":
        update_contact()
    elif choice == "4":
        query_contacts()
    elif choice == "5":
        delete_contact()
    elif choice == "6":
        break
