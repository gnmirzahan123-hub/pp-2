    import psycopg2
    import csv
    import json

    # Подключение к базе данных
    def get_connection():
        return psycopg2.connect(
            dbname="phonebook5",  # Замените на название вашей базы данных
            user="postgres",  # Замените на ваш логин
            password="your_password",  # Замените на ваш пароль
            host="127.0.0.1",  # Это может быть localhost или ваш сервер
            port="5432"
        )

    # Функция добавления группы
    def add_group(cursor):
        group_name = input("Введите название группы: ")
        cursor.execute("CALL add_group(%s)", (group_name,))
        print(f"Группа '{group_name}' добавлена успешно.")

    # Функция перемещения контакта в группу
    def move_to_group(cursor):
        contact_name = input("Введите имя контакта: ")
        group_name = input("Введите название группы: ")
        cursor.execute("CALL move_to_group(%s, %s)", (contact_name, group_name))
        print(f"Контакт '{contact_name}' перемещён в группу '{group_name}'.")

    # Функция добавления телефона контакту
    def add_phone(cursor):
        contact_name = input("Введите имя контакта: ")
        phone = input("Введите телефон: ")
        phone_type = input("Введите тип телефона: ")
        cursor.execute("CALL add_phone(%s, %s, %s)", (contact_name, phone, phone_type))
        print(f"Телефон '{phone}' добавлен к контакту '{contact_name}'.")

    # Функция для добавления или обновления контакта
    def upsert_contact(cursor):
        name = input("Введите имя контакта: ")
        email = input("Введите email контакта: ")
        birthday = input("Введите день рождения (YYYY-MM-DD): ")
        cursor.execute("INSERT INTO phonebook(name, email, birthday) VALUES(%s, %s, %s) ON CONFLICT(name) DO UPDATE SET email = %s, birthday = %s", 
                    (name, email, birthday, email, birthday))
        print(f"Контакт '{name}' добавлен или обновлён.")

    # Функция для массовой вставки контактов
    def insert_many_contacts(cursor):
        names = input("Введите имена через запятую: ").split(",")
        emails = input("Введите emails через запятую: ").split(",")
        birthdays = input("Введите дни рождения через запятую (YYYY-MM-DD): ").split(",")
        for i in range(len(names)):
            cursor.execute("INSERT INTO phonebook(name, email, birthday) VALUES(%s, %s, %s) ON CONFLICT(name) DO UPDATE SET email = %s, birthday = %s", 
                        (names[i], emails[i], birthdays[i], emails[i], birthdays[i]))
        print("Массовая вставка выполнена.")

    # Функция для поиска контактов по шаблону
    def search_contacts(cursor):
        pattern = input("Введите шаблон для поиска (по имени или email): ")
        cursor.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
        result = cursor.fetchall()
        if result:
            print("Найденные контакты:")
            for contact in result:
                print(contact)
        else:
            print("Контакты не найдены.")

    # Функция для удаления контакта
    def delete_contact(cursor):
        mode = input("Удалить по (1) имени или (2) email: ")
        if mode == "1":
            name = input("Введите имя: ")
            cursor.execute("DELETE FROM phonebook WHERE name = %s", (name,))
        else:
            email = input("Введите email: ")
            cursor.execute("DELETE FROM phonebook WHERE email = %s", (email,))
        print("Контакт удалён.")

    # Пагинация для вывода контактов
    def paginated_view(cursor):
        limit = int(input("Сколько записей показывать? "))
        offset = int(input("С какого места начать вывод? "))
        cursor.execute("SELECT * FROM phonebook LIMIT %s OFFSET %s", (limit, offset))
        result = cursor.fetchall()
        if result:
            for contact in result:
                print(contact)
        else:
            print("Нет записей для отображения.")

    # Экспорт контактов в JSON
    def export_to_json(cursor):
        cursor.execute("SELECT * FROM phonebook")
        contacts = cursor.fetchall()
        with open("contacts.json", "w") as f:
            json.dump(contacts, f)
        print("Контакты экспортированы в contacts.json.")

    # Импорт контактов из JSON
    def import_from_json(cursor):
        with open("contacts.json", "r") as f:
            contacts = json.load(f)
        for contact in contacts:
            cursor.execute("INSERT INTO phonebook(id, name, email, birthday) VALUES(%s, %s, %s, %s) ON CONFLICT(id) DO UPDATE SET name = %s, email = %s, birthday = %s", 
                        (contact[0], contact[1], contact[2], contact[3], contact[1], contact[2], contact[3]))
        print("Контакты импортированы из contacts.json.")

    # Экспорт в CSV
    def export_to_csv(cursor):
        cursor.execute("SELECT * FROM phonebook")
        contacts = cursor.fetchall()
        with open("contacts.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Email", "Birthday"])  # Заголовки
            writer.writerows(contacts)
        print("Контакты экспортированы в contacts.csv.")

    # Импорт из CSV
    def import_from_csv(cursor):
        with open("contacts.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Пропустить заголовок
            for row in reader:
                id, name, email, birthday = row
                cursor.execute("INSERT INTO phonebook(id, name, email, birthday) VALUES(%s, %s, %s, %s) ON CONFLICT(id) DO UPDATE SET name = %s, email = %s, birthday = %s", 
                            (id, name, email, birthday, name, email, birthday))
        print("Контакты импортированы из contacts.csv.")

    # Основное меню
    def start():
        conn = get_connection()
        cursor = conn.cursor()

        while True:
            print("\n--- PhoneBook Menu ---")
            print("1. Добавить/обновить контакт")
            print("2. Массовая вставка")
            print("3. Найти по шаблону")
            print("4. Удалить контакт")
            print("5. Добавить группу")
            print("6. Переместить контакт в группу")
            print("7. Добавить телефон контакту")
            print("8. Пагинация")
            print("9. Экспорт в JSON")
            print("10. Импорт из JSON")
            print("11. Экспорт в CSV")
            print("12. Импорт из CSV")
            print("13. Показать все контакты")
            print("14. Обновить контакт по email")
            print("15. Удалить все контакты")
            print("16. Показать группы контактов")
            print("17. Выйти")

            choice = input("Выберите действие: ")

            if choice == "1":
                upsert_contact(cursor)
            elif choice == "2":
                insert_many_contacts(cursor)
            elif choice == "3":
                search_contacts(cursor)
            elif choice == "4":
                delete_contact(cursor)
            elif choice == "5":
                add_group(cursor)
            elif choice == "6":
                move_to_group(cursor)
            elif choice == "7":
                add_phone(cursor)
            elif choice == "8":
                paginated_view(cursor)
            elif choice == "9":
                export_to_json(cursor)
            elif choice == "10":
                import_from_json(cursor)
            elif choice == "11":
                export_to_csv(cursor)
            elif choice == "12":
                import_from_csv(cursor)
            elif choice == "13":
                cursor.execute("SELECT * FROM phonebook")
                result = cursor.fetchall()
                for contact in result:
                    print(contact)
            elif choice == "14":
                email = input("Введите email для обновления контакта: ")
                new_email = input("Введите новый email: ")
                cursor.execute("UPDATE phonebook SET email = %s WHERE email = %s", (new_email, email))
                print(f"Email обновлён для контакта {email}.")
            elif choice == "15":
                cursor.execute("DELETE FROM phonebook")
                print("Все контакты удалены.")
            elif choice == "16":
                cursor.execute("SELECT * FROM groups")
                result = cursor.fetchall()
                for group in result:
                    print(group)
            elif choice == "17":
                cursor.close()
                conn.commit()
                conn.close()
                break
            else:
                print("Некорректный выбор, попробуйте снова.")

    if __name__ == "__main__":
        start()