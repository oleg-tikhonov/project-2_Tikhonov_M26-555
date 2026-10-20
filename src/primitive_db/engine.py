import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import (  # noqa: E501
    DB_FILE,
    create_table,
    delete,
    drop_table,
    insert,
    select,
    update,
)
from primitive_db.parser import parse_clause
from primitive_db.utils import (  # noqa: E501
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)


def show_menu():
    print("- <command> exit: выйти из программы")
    print("- <command> help: справочная информация")

def welcome():
    print("Первая попытка запустить проект!")
    print("\n***")
    show_menu()

    while True:
        command = prompt.string("Введите команду: ")

        if command == "help":
            print()
            show_menu()
        elif command == "exit":
            break

def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    print("Первая попытка запустить проект!")
    print_help()

    while True:
        metadata = load_metadata(DB_FILE)
        
        command_line = prompt.string(">>>Введите команду: ")
        if command_line is None:
            break
        
        command_line = command_line.strip()
        
        if not command_line:
            continue

        try:
            args = shlex.split(command_line)
        except ValueError:
            print("Ошибка парсинга команды. Проверьте правильность ввода.")
            continue

        command = args[0]

        if command == "exit":
            break
            
        elif command == "help":
            print_help()
            
        elif command == "list_tables":
            if metadata:
                print("- ")
                for table in metadata:
                    print(table)
            else:
                print("-")
                
        elif command == "create_table":
            if len(args) < 2:
                print(f"Некорректное значение: {command_line}. Попробуйте снова.")
                continue
                
            table_name = args[1]
            columns = args[2:]
            old_tables = list(metadata.keys())
            
            metadata = create_table(metadata, table_name, columns)
            
            if table_name not in old_tables and table_name in metadata:
                save_metadata(DB_FILE, metadata)
                
        elif command == "drop_table":
            if len(args) != 2:
                print(f"Некорректное значение: {command_line}. Попробуйте снова.")
                continue
                
            table_name = args[1]
            old_tables = list(metadata.keys())
            
            metadata = drop_table(metadata, table_name)
            
            if table_name in old_tables and table_name not in metadata:
                save_metadata(DB_FILE, metadata)
        
        elif command == "insert":
            parts = command_line[11:].strip().split(" values ", 1)
            if len(parts) == 2:
                table_name = parts[0].strip()
                val_str = parts[1].strip()
                
                if val_str.startswith("(") and val_str.endswith(")"):
                    val_str = val_str[1:-1]
                    raw_vals = [v.strip() for v in val_str.split(",")]
                    clean_vals = []
                    
                    for v in raw_vals:
                        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")): # noqa: E501
                            clean_vals.append(v[1:-1])
                        else:
                            clean_vals.append(v)
                            
                    data = insert(metadata, table_name, clean_vals)
                    if data is not None:
                        print(f'Запись успешно добавлена в таблицу "{table_name}".')
                else:
                    print("Ошибка синтаксиса insert.")
            else:
                print("Ошибка синтаксиса insert.")

        elif command == "select":
            remainder = command_line[11:].strip()
            
            if " where " in remainder.lower():
                idx = remainder.lower().find(" where ")
                table_name = remainder[:idx].strip()
                where_str = remainder[idx+7:].strip()
            else:
                table_name = remainder.strip()
                where_str = None

            if table_name not in metadata:
                print(f"Ошибка: Таблица '{table_name}' не найдена.")
                continue
                
            data = load_table_data(table_name)
            where_clause = parse_clause(where_str) if where_str else {}
            
            result = select(data, where_clause)
            
            if result:
                pt = PrettyTable()
                pt.field_names = list(metadata[table_name].keys())
                for row in result:
                    pt.add_row([row.get(k, "") for k in pt.field_names])
                print(pt)
            else:
                print("Записи не найдены.")

        elif command == "update":
            remainder = command_line[6:].strip()
            
            if " set " in remainder.lower() and " where " in remainder.lower():
                set_idx = remainder.lower().find(" set ")
                where_idx = remainder.lower().find(" where ", set_idx)
                
                table_name = remainder[:set_idx].strip()
                set_str = remainder[set_idx+5:where_idx].strip()
                where_str = remainder[where_idx+7:].strip()
                
                if table_name not in metadata:
                    print(f"Ошибка: Таблица '{table_name}' не найдена.")
                    continue
                    
                data = load_table_data(table_name)
                set_clause = parse_clause(set_str)
                where_clause = parse_clause(where_str)
                
                updated_data = update(data, set_clause, where_clause)
                save_table_data(table_name, updated_data)
                print(f'Записи в таблице "{table_name}" успешно обновлены.')
            else:
                print("Ошибка синтаксиса update.")

        elif command == "delete":
            remainder = command_line[11:].strip()
            
            if " where " in remainder.lower():
                idx = remainder.lower().find(" where ")
                table_name = remainder[:idx].strip()
                where_str = remainder[idx+7:].strip()
                
                if table_name not in metadata:
                    print(f"Ошибка: Таблица '{table_name}' не найдена.")
                    continue
                    
                data = load_table_data(table_name)
                where_clause = parse_clause(where_str)
                
                updated_data = delete(data, where_clause)
                save_table_data(table_name, updated_data)
                print(f'Записи успешно удалены из таблицы "{table_name}".')
            else:
                print("Ошибка синтаксиса delete.")

        else:
            print(f"Функции {command} нет. Попробуйте снова.")
