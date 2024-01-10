import sqlite3

connection = sqlite3.connect("Имя БД")
cursor = connection.cursor()


def create_table(table_name: str, columns: tuple) -> None:
    """
    Создает таблицу с указанным именем и столбцами.

    table_name: Имя таблицы\n
    columns: Список кортежей, где каждый кортеж содержит (имя_столбца,
    тип_столбца)
    """
    columns_str = ", ".join([f"{col[0]} {col[1]}" for col in columns])
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")
    connection.commit()


def add_record(table_name: str, values: dict) -> None:
    """
    Добавляет запись в указанную таблицу.

    table_name: Имя таблицы\n
    values: Словарь, где ключи - это имена столбцов, а значения -
    соответствующие значения
    """
    columns = ", ".join(values.keys())
    placeholders = ", ".join(["?" for _ in values.keys()])
    cursor.execute(f"INSERT INTO {table_name} ({columns})"
                   f"VALUES ({placeholders})", tuple(values.values()))
    connection.commit()


def exists_in_table(table_name: str, condition: tuple) -> bool:
    """
    Проверяет, существует ли запись в указанной таблице на основе заданного
    условия.

    table_name: Имя таблицы\n
    condition: Кортеж, где первый элемент - это имя столбца, а второй
    элемент - значение для проверки\n
    True, если запись существует, иначе False
    """
    cursor.execute(f"SELECT 1 FROM {table_name} WHERE {condition[0]} = ?",
                   (condition[1],))
    result = cursor.fetchone()
    return result is not None


def get_column_value_by_name(table_name: str, column_to_get: str,
                             condition: tuple) -> None:
    """
    Получает значение определенного столбца в таблице на основе условия.

    table_name: Имя таблицы \n
    column_to_get: Имя столбца для извлечения\n
    condition: Кортеж, где первый элемент - это имя столбца, а второй
    элемент - значение для проверки\n
    Значение указанного столбца или None, если не найдено
    """
    cursor.execute(f"SELECT {column_to_get} FROM {table_name}"
                   f"WHERE {condition[0]} = ?", (condition[1],))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None


def update_column_value(table_name: str, column_to_update: str,
                        new_value, condition: tuple) -> None:
    """
    Обновляет значение определенного столбца в таблице на основе условия.

    table_name: Имя таблицы \n
    column_to_update: Имя столбца для обновления\n
    new_value: Новое значение для установки\n
    condition: Кортеж, где первый элемент - это имя столбца, а второй
    элемент - значение для проверки
    """
    cursor.execute(f'UPDATE {table_name} SET {column_to_update} = ?'
                   f'WHERE {condition[0]} = ?',
                   (new_value, condition[1]))
    connection.commit()
