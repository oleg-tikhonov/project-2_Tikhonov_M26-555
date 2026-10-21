import json
import os

from primitive_db.constants import DATA_DIR


def load_metadata(filepath):
    """Загружает метаданные базы данных (структуру таблиц) из файла."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_metadata(filepath, data):
    """Сохраняет структуру таблиц (метаданные) в JSON-файл."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_table_data(table_name):
    """Загружает все записи конкретной таблицы из её JSON-файла."""
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def save_table_data(table_name, data):
    """Сохраняет список записей в файл таблицы, создавая data при необходимости."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)