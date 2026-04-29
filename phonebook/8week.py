import psycopg2
import json
import csv

# --- Подключение к базе данных ---
def get_connection():
    return psycopg2.connect(
        dbname="phonebook",
        user="postgres",
        password="mns2007Nur123",
        host="127.0.0.1",
        port="5432"
    )

# --- Настройка базы данных ---
def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Создание таблицы для групп
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS groups (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE
    );
    """)

    # Создание таблицы для контактов (phonebook)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE,
        phone VARCHAR(20),
        email VARCHAR(100),
        birthday DATE,
        group_id INT REFERENCES groups(id)
    );
    """)

    # Создание таблицы для телефонов (phones)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS phones (
        id SERIAL PRIMARY KEY,
        contact_id INT REFERENCES phonebook(id),
        phone VARCHAR(20),
        phone_type VARCHAR(20) -- E.g., mobile, home, etc.
    );
    """)

    # Процедура для массовой вставки контактов
    cursor.execute("""
    CREATE OR REPLACE PROCEDURE insert_many_contacts(
        p_names TEXT[], 
        p_phones TEXT[], 
        p_emails TEXT[], 
        p_birthdays TEXT[]
    )
    LANGUAGE plpgsql AS $$
    DECLARE
        i INT;
    BEGIN
        FOR i IN 1..array_length(p_names, 1) LOOP
            INSERT INTO phonebook(name, phone, email, birthday) 
            VALUES (
                p_names[i], 
                p_phones[i], 
                p_emails[i], 
                TO_DATE(p_birthdays[i], 'YYYY-MM-DD')
            )
            ON CONFLICT (name) 
            DO UPDATE 
            SET phone = EXCLUDED.phone, 
                email = EXCLUDED.email, 
                birthday = EXCLUDED.birthday;
        END LOOP;
    END;
    $$;
    """)

    # Процедура удаления контакта по имени или телефону
    cursor.execute("""
    CREATE OR REPLACE PROCEDURE delete_contact(p_name VARCHAR DEFAULT NULL, p_phone VARCHAR DEFAULT NULL)
    LANGUAGE plpgsql AS $$
    BEGIN
        IF p_name IS NOT NULL THEN
            DELETE FROM phonebook WHERE name = p_name;
        ELSIF p_phone IS NOT NULL THEN
            DELETE FROM phonebook WHERE phone = p_phone;
        ELSE
            RAISE NOTICE 'Нужно указать имя или телефон для удаления';
        END IF;
    END;
    $$;
    """)

    conn.commit()
    cursor.close()
    conn.close()

# --- Консольный интерфейс ---
def start():
    setup_database()
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Добавить/обновить контакт")
        print("2. Массовая вставка")
        print("3. Найти по шаблону")
        print("4. Показать с пагинацией")
        print("5. Удалить контакт")
        print("6. Показать все контакты")
        print("7. Поиск по email")
        print("8. Фильтровать по группе")
        print("9. Сортировать контакты")
        print("10. Экспортировать в JSON")
        print("11. Импортировать из JSON")
        print("12. Импортировать из CSV")
        print("13. Выйти")

        choice = input("Выберите действие: ")

        conn = get_connection()
        cursor = conn.cursor()

        if choice == "1":
            name = input("Введите имя: ")
            phone = input("Введите телефон: ")
            email = input("Введите email: ")
            birthday = input("Введите дату рождения (YYYY-MM-DD): ")
            cursor.execute("CALL upsert_contact(%s, %s, %s, %s)", (name, phone, email, birthday))
            conn.commit()
            print("Контакт добавлен/обновлён.")

        elif choice == "2":
            names = input("Введите имена через запятую: ").split(",")
            phones = input("Введите телефоны через запятую: ").split(",")
            emails = input("Введите emails через запятую: ").split(",")
            birthdays = input("Введите даты рождения через запятую (формат YYYY-MM-DD): ").split(",")
            cursor.execute("CALL insert_many_contacts(%s, %s, %s, %s)", (names, phones, emails, birthdays))
            conn.commit()
            print("Массовая вставка выполнена.")

        elif choice == "3":
            pattern = input("Введите шаблон поиска: ")
            cursor.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
            print(cursor.fetchall())

        elif choice == "4":
            limit = int(input("Сколько записей показать: "))
            offset = int(input("С какой позиции начать: "))
            cursor.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
            print(cursor.fetchall())

        elif choice == "5":
            mode = input("Удалить по (1) имени или (2) телефону: ")
            if mode == "1":
                name = input("Введите имя: ")
                cursor.execute("CALL delete_contact(p_name := %s)", (name,))
            elif mode == "2":
                phone = input("Введите телефон: ")
                cursor.execute("CALL delete_contact(p_phone := %s)", (phone,))
            conn.commit()
            print("Контакт удалён.")

        elif choice == "6":
            cursor.execute("SELECT * FROM phonebook ORDER BY id")
            print(cursor.fetchall())

        elif choice == "7":
            email_pattern = input("Введите email для поиска: ")
            cursor.execute("SELECT * FROM phonebook WHERE email ILIKE %s", ('%' + email_pattern + '%',))
            print(cursor.fetchall())

        elif choice == "8":
            group = input("Введите название группы для фильтрации: ")
            cursor.execute("SELECT * FROM phonebook WHERE group_id = (SELECT id FROM groups WHERE name = %s)", (group,))
            print(cursor.fetchall())

        elif choice == "9":
            sort_by = input("Выберите сортировку: (1) по имени, (2) по дате рождения, (3) по дате добавления: ")
            if sort_by == "1":
                cursor.execute("SELECT * FROM phonebook ORDER BY name")
            elif sort_by == "2":
                cursor.execute("SELECT * FROM phonebook ORDER BY birthday")
            elif sort_by == "3":
                cursor.execute("SELECT * FROM phonebook ORDER BY id")
            print(cursor.fetchall())

        elif choice == "10":
            cursor.execute("SELECT * FROM phonebook")
            contacts = cursor.fetchall()
            with open('contacts.json', 'w') as json_file:
                json.dump(contacts, json_file, default=str)
            print("Экспорт в JSON выполнен.")

        elif choice == "11":
            with open('contacts.json', 'r') as json_file:
                contacts = json.load(json_file)
                for contact in contacts:
                    cursor.execute("CALL upsert_contact(%s, %s, %s, %s)", (contact[1], contact[2], contact[3], contact[4]))
            conn.commit()
            print("Импорт из JSON выполнен.")

        elif choice == "12":
            with open('contacts.csv', 'r') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    cursor.execute("CALL upsert_contact(%s, %s, %s, %s)", (row[0], row[1], row[2], row[3]))
            conn.commit()
            print("Импорт из CSV выполнен.")

        elif choice == "13":
            cursor.close()
            conn.close()
            break

        cursor.close()
        conn.close()

if __name__ == "__main__":
    start()