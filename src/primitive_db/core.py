from primitive_db.utils import load_table_data, save_table_data
from primitive_db.decorators import confirm_action, create_cacher, handle_db_errors, log_time

DB_FILE = "db_meta.json"
select_cacher = create_cacher()

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

@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata, table_name):
    
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata 

@log_time
@handle_db_errors
def insert(metadata, table_name, values):
    
    columns = metadata[table_name]
    
    col_names = list(columns.keys())[1:]
    col_types = list(columns.values())[1:]

    if len(values) != len(col_names):
        print(f"Ошибка: Ожидалось {len(col_names)} значений, а получено {len(values)}.")
        return None

    new_record = {}

    for col_name, col_type, val in zip(col_names, col_types, values):
        try:
            if col_type == "int":
                new_record[col_name] = int(val)
            elif col_type == "float":
                new_record[col_name] = float(val)
            elif col_type == "bool":
                val_lower = str(val).lower()
                if val_lower in ("true", "1", "yes"):
                    new_record[col_name] = True
                elif val_lower in ("false", "0", "no"):
                    new_record[col_name] = False
                else:
                    raise ValueError
            else:
                new_record[col_name] = str(val)
        except ValueError:
            print(f"Ошибка: Значение '{val}' не подходит для типа {col_type} (столбец '{col_name}').") # noqa: E501
            return None

    data = load_table_data(table_name)

    if data:
        new_id = max(row["ID"] for row in data) + 1
    else:
        new_id = 1

    final_record = {"ID": new_id}
    final_record.update(new_record)

    data.append(final_record)
    save_table_data(table_name, data)

    return data

@log_time
def select(table_data, where_clause=None):
    if not where_clause:
        return table_data

    cache_key = tuple(sorted(where_clause.items()))

    def get_data():
        result = []
        for row in table_data:
            match = True
            for key, value in where_clause.items():
                if row.get(key) != value:
                    match = False
                    break
            if match:
                result.append(row)
        return result

    return select_cacher(cache_key, get_data)

def update(table_data, set_clause, where_clause):
    for row in table_data:
        match = True
        for key, value in where_clause.items():
            if row.get(key) != value:
                match = False
                break

        if match:
            for set_key, set_value in set_clause.items():
                if set_key in row:
                    row[set_key] = set_value

    return table_data

@confirm_action("удаление записей")
def delete(table_data, where_clause):
    result = []
    for row in table_data:
        match = True
        for key, value in where_clause.items():
            if row.get(key) != value:
                match = False
                break

        if not match:
            result.append(row)

    return result