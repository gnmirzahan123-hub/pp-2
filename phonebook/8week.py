import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="1",
        user="postgres",
        password="mns2007Nur123",
        host="127.0.0.1",
        port="5432"
    )

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE,
        phone VARCHAR(20)
    );
    """)

    # Функция поиска по шаблону
    cursor.execute("""
    CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p text)
    RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
    BEGIN
        RETURN QUERY
        SELECT pb.id, pb.name, pb.phone
        FROM phonebook pb
        WHERE pb.name ILIKE '%' || p || '%'
           OR pb.phone ILIKE '%' || p || '%';
    END;
    $$ LANGUAGE plpgsql;
    """)

    # Процедура вставки/обновления
    cursor.execute("""
    CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
    LANGUAGE plpgsql AS $$
    BEGIN
        IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
            UPDATE phonebook SET phone = p_phone WHERE name = p_name;
        ELSE
            INSERT INTO phonebook(name, phone) VALUES(p_name, p_phone);
        END IF;
    END;
    $$;
    """)

    # Процедура массовой вставки
    cursor.execute("""
    CREATE OR REPLACE PROCEDURE insert_many_contacts(p_names TEXT[], p_phones TEXT[])
    LANGUAGE plpgsql AS $$
    DECLARE
        i INT;
        bad_data TEXT[] := '{}';
    BEGIN
        FOR i IN 1..array_length(p_names, 1) LOOP
            IF p_phones[i] ~ '^[0-9]+$' THEN
                IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_names[i]) THEN
                    UPDATE phonebook SET phone = p_phones[i] WHERE name = p_names[i];
                ELSE
                    INSERT INTO phonebook(name, phone) VALUES(p_names[i], p_phones[i]);
                END IF;
            ELSE
                bad_data := array_append(bad_data, p_names[i] || ':' || p_phones[i]);
            END IF;
        END LOOP;
        RAISE NOTICE 'Некорректные данные: %', bad_data;
    END;
    $$;
    """)

    # Функция с пагинацией
    cursor.execute("""
    CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
    RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
    BEGIN
        RETURN QUERY
        SELECT pb.id, pb.name, pb.phone
        FROM phonebook pb
        ORDER BY pb.id
        LIMIT p_limit OFFSET p_offset;
    END;
    $$ LANGUAGE plpgsql;
    """)

    # Процедура удаления
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

# --- Меню PhoneBook ---
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
        print("7. Выйти")

        choice = input("Выберите действие: ")

        conn = get_connection()
        cursor = conn.cursor()

        if choice == "1":
            name = input("Введите имя: ")
            phone = input("Введите телефон: ")
            cursor.execute("CALL upsert_contact(%s, %s)", (name, phone))
            conn.commit()
            print("Контакт добавлен/обновлён.")

        elif choice == "2":
            names = input("Введите имена через запятую: ").split(",")
            phones = input("Введите телефоны через запятую: ").split(",")
            cursor.execute("CALL insert_many_contacts(%s, %s)", (names, phones))
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
            else:
                phone = input("Введите телефон: ")
                cursor.execute("CALL delete_contact(p_phone := %s)", (phone,))
            conn.commit()
            print("Контакт удалён.")

        elif choice == "6":
            cursor.execute("SELECT * FROM phonebook ORDER BY id")
            print(cursor.fetchall())

        elif choice == "7":
            cursor.close()
            conn.close()
            break

        cursor.close()
        conn.close()

if __name__ == "__main__":
    start()
