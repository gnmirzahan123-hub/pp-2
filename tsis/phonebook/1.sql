-- Таблица для контактов
CREATE TABLE IF NOT EXISTS phonebook (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE,
    email VARCHAR(100),
    birthday DATE
);

-- Таблица для телефонов
CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INT,
    phone VARCHAR(20),
    phone_type VARCHAR(20),
    FOREIGN KEY (contact_id) REFERENCES phonebook(id)
);

-- Таблица для групп
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE
);

-- Таблица для связи контактов с группами
CREATE TABLE IF NOT EXISTS contact_groups (
    contact_id INT,
    group_id INT,
    PRIMARY KEY (contact_id, group_id),
    FOREIGN KEY (contact_id) REFERENCES phonebook(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

-- Функция для добавления или обновления контакта
CREATE OR REPLACE FUNCTION upsert_contact(p_name VARCHAR, p_email VARCHAR, p_birthday DATE)
RETURNS VOID AS $$
BEGIN
    -- Если контакт существует, обновить его данные
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook SET email = p_email, birthday = p_birthday WHERE name = p_name;
    ELSE
        -- Если не существует, вставить новый контакт
        INSERT INTO phonebook(name, email, birthday) VALUES (p_name, p_email, p_birthday);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Функция для добавления телефона к контакту
CREATE OR REPLACE FUNCTION add_phone(p_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
RETURNS VOID AS $$
BEGIN
    -- Вставка телефона для существующего контакта
    INSERT INTO phones(contact_id, phone, phone_type)
    SELECT id, p_phone, p_type FROM phonebook WHERE name = p_name;
END;
$$ LANGUAGE plpgsql;

-- Функция для перемещения контакта в группу
CREATE OR REPLACE FUNCTION move_to_group(p_name VARCHAR, p_group_name VARCHAR)
RETURNS VOID AS $$
DECLARE
    group_id INT;  -- Объявление переменной для хранения ID группы
BEGIN
    -- Создание группы, если её нет
    INSERT INTO groups(name) 
    VALUES (p_group_name) 
    ON CONFLICT (name) DO NOTHING;
    
    -- Получение id группы
    SELECT id INTO group_id 
    FROM groups 
    WHERE name = p_group_name
    LIMIT 1;  -- Ограничиваем результат одним значением, чтобы не было ошибок

    -- Добавление контакта в группу
    INSERT INTO contact_groups(contact_id, group_id)
    SELECT id, group_id 
    FROM phonebook 
    WHERE name = p_name
    LIMIT 1;  -- Ограничиваем результат одним значением, чтобы не было ошибок
END;
$$ LANGUAGE plpgsql;

-- Функция для поиска контактов по шаблону
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(id INT, name VARCHAR, email VARCHAR, birthday DATE, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name, p.email, p.birthday, ph.phone
    FROM phonebook p
    LEFT JOIN phones ph ON p.id = ph.contact_id
    WHERE p.name ILIKE '%' || p_query || '%'
       OR p.email ILIKE '%' || p_query || '%'
       OR ph.phone ILIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;

-- Функция для получения контактов с пагинацией
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name VARCHAR, email VARCHAR, birthday DATE, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name, p.email, p.birthday, ph.phone
    FROM phonebook p
    LEFT JOIN phones ph ON p.id = ph.contact_id
    ORDER BY p.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- Функция для удаления контакта по имени
CREATE OR REPLACE FUNCTION delete_contact(p_name VARCHAR)
RETURNS VOID AS $$
BEGIN
    DELETE FROM phonebook WHERE name = p_name;
END;
$$ LANGUAGE plpgsql;

-- Процедура массового добавления контактов
CREATE OR REPLACE PROCEDURE insert_many_contacts(p_names TEXT[], p_phones TEXT[], p_emails TEXT[], p_birthdays DATE[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        -- Вставка или обновление каждого контакта
        CALL upsert_contact(p_names[i], p_emails[i], p_birthdays[i]);

        -- Вставка телефона для контакта
        CALL add_phone(p_names[i], p_phones[i], 'mobile');
    END LOOP;
END;
$$;
