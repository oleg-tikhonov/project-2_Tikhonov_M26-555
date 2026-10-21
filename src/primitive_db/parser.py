def parse_clause(clause_str):
    """
    Разбирает строку условий (например, 'age=30, name="Oleg"') 
    и возвращает словарь с приведенными типами данных.
    """
    if not clause_str:
        return {}

    result = {}
    pairs = clause_str.split(",")

    for pair in pairs:
        if "=" not in pair:
            continue

        key, value_str = pair.split("=", 1)
        key = key.strip()
        value_str = value_str.strip()

        has_double_quotes = value_str.startswith('"') and value_str.endswith('"')
        has_single_quotes = value_str.startswith("'") and value_str.endswith("'")

        if has_double_quotes or has_single_quotes:
            result[key] = value_str[1:-1]
        elif value_str.lower() == "true":
            result[key] = True
        elif value_str.lower() == "false":
            result[key] = False
        elif "." in value_str:
            try:
                result[key] = float(value_str)
            except ValueError:
                result[key] = value_str
        else:
            try:
                result[key] = int(value_str)
            except ValueError:
                result[key] = value_str

    return result