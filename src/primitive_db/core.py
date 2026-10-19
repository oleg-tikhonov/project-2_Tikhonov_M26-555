DB_FILE = "db_meta.json"

def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    table_columns = {"ID": "int"}
    valid_types = {"int", "str", "bool"}

    for col in columns:
        if ":" not in col:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata
            
        c_name, c_type = col.split(":", 1)
        
        if c_type not in valid_types:
            print(f"Некорректное значение: {c_type}. Попробуйте снова.")
            return metadata
            
        table_columns[c_name] = c_type

    metadata[table_name] = table_columns
    
    cols_str = ", ".join(f"{k}:{v}" for k, v in table_columns.items())
    print(f'Таблица "{table_name}" успешно создана со столбцами: {cols_str}')
    
    return metadata


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    
    return metadata 