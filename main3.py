"""
Завдання:
розробити Python-скрипт для аналізу файлів логів. Скрипт повинен вміти читати лог-файл, 
переданий як аргумент командного рядка, і виводити статистику за рівнями логування 
наприклад, INFO, ERROR, DEBUG. Також користувач може вказати рівень логування як другий 
аргумент командного рядка, щоб отримати всі записи цього рівня.
Лог-аналітик для файлів логів.

Скрипт:
- Зчитує лог-файл, переданий як аргумент командного рядка.
- Підраховує кількість записів за рівнями логування (INFO, ERROR, DEBUG, WARNING).
- Опціонально фільтрує записи за певним рівнем логування, якщо вказано другий аргумент.

Приклад запуску:
    python3 main3.py logfile.log
    python3 main3.py logfile.log error

Log Analyzer  - аналізує лог-файли та виводить статистику за рівнями логування.
Можна вказати опційно рівень для детального перегляду.
"""

import sys
from typing import List, Dict

# Константа допустимих рівнів логів
LOG_LEVELS = ["INFO", "DEBUG", "ERROR", "WARNING"]

# Кольори для терміналу (ANSI)
COLORS = {
    "INFO": "\033[92m",    # зелений
    "DEBUG": "\033[94m",   # синій
    "ERROR": "\033[91m",   # червоний
    "WARNING": "\033[93m", # жовтий
    "ENDC": "\033[0m"
}


def parse_log_line(line: str) -> Dict[str, str]:
    """
    Розбираємо рядок лог-файлу на компоненти: дата, час, рівень логування, повідомлення.
    """
    parts = line.strip().split(maxsplit=3)
    if len(parts) < 4:
        raise ValueError(f"Неправильний формат рядка: {line}")
    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2].upper(),
        "message": parts[3]
    }


def load_logs(file_path: str) -> List[Dict[str, str]]:
    """
    Завантажуємо лог-файл і повертаємо список словників.
    """
    logs = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    logs.append(parse_log_line(line))
    except FileNotFoundError:
        print(f"Файл не знайдено: {file_path}")
        sys.exit(1)
    except ValueError as ve:
        print(f"Помилка формату рядка логу: {ve}")
        sys.exit(1)
    except OSError as oe:
        print(f"Помилка при роботі з файлом: {oe}")
        sys.exit(1)
    return logs


def filter_logs_by_level(logs: List[Dict[str, str]], level: str) -> List[Dict[str, str]]:
    """
    Повертаємо список логів заданого рівня.
    """
    level = level.upper()
    return [log for log in logs if log["level"] == level]


def count_logs_by_level(logs: List[Dict[str, str]]) -> Dict[str, int]:
    """
    Підраховуємо кількість записів для кожного рівня логування.
    """
    counts = {}
    for log in logs:
        counts[log["level"]] = counts.get(log["level"], 0) + 1
    return counts


def display_log_counts(counts: Dict[str, int]) -> None:
    """
    Виводимо статистику в форматованій таблиці з кольоровим виділенням.
    """
    print("\nРівень логування | Кількість")
    print("-----------------|----------")
    for level in LOG_LEVELS:
        color = COLORS.get(level, "")
        endc = COLORS["ENDC"]
        print(f"{color}{level:<16} | {counts.get(level, 0)}{endc}")


def main():
    """Головна функція скрипту."""
    if len(sys.argv) < 2:
        print("Використання: python main.py <шлях до файлу логів> [рівень]")
        sys.exit(1)

    file_path = sys.argv[1]
    filter_level = sys.argv[2].upper() if len(sys.argv) > 2 else None

    if filter_level and filter_level not in LOG_LEVELS:
        print(f"Невідомий рівень логування: {filter_level}")
        print(f"Допустимі рівні: {', '.join(LOG_LEVELS)}")
        sys.exit(1)

    logs = load_logs(file_path)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if filter_level:
        filtered_logs = filter_logs_by_level(logs, filter_level)
        if filtered_logs:
            print(f"\nДеталі логів для рівня '{filter_level}':")
            for log in filtered_logs:
                color = COLORS.get(filter_level, "")
                endc = COLORS["ENDC"]
                print(f"{color}{log['date']} {log['time']} - {log['message']}{endc}")
        else:
            print(f"\nЗаписи рівня '{filter_level}' відсутні.")


if __name__ == "__main__":
    main()
