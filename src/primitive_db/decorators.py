import time
from functools import wraps


def handle_db_errors(func):
    """Декоратор для перехвата и обработки стандартных ошибок базы данных."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. Возможно, база данных не инициализирована.") # noqa: E501
        except KeyError as e:
            print(f"Ошибка: Таблица {e} не найдена.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    return wrapper

def confirm_action(action_name):
    """Декоратор для запроса подтверждения перед выполнением опасных действий."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ').strip().lower() # noqa: E501
            if answer == 'y':
                return func(*args, **kwargs)
            else:
                print("Операция отменена.")
                return args[0] if args else None
        return wrapper
    return decorator

def log_time(func):
    """Декоратор для замера и вывода времени выполнения функции."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        
        execution_time = end_time - start_time
        print(f"Функция {func.__name__} выполнилась за {execution_time:.3f} секунд.")
        
        return result
    return wrapper

def create_cacher():
    """Создает замыкание для кэширования результатов запросов (select)."""
    cache = {}

    def cache_result(key, value_func):
        if key in cache:
            print(f"[*] Возвращаем результат из кэша для запроса: {key}")
            return cache[key]
        
        result = value_func()
        cache[key] = result
        return result

    return cache_result