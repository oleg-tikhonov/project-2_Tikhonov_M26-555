import shlex

import prompt

from primitive_db.core import DB_FILE, create_table, drop_table
from primitive_db.utils import load_metadata, save_metadata


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
                
        else:
            print(f"Функции {command} нет. Попробуйте снова.")
            