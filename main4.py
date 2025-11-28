'''
Завдання:
доробити консольного бота помічника з попереднього домашнього завдання 
та додати обробку помилок за допомогою декораторів.

Вимоги:
всі помилки введення користувача повинні оброблятися за допомогою декоратора 
input_error. Цей декоратор відповідає за повернення користувачеві повідомлень 
типу "Enter user name", "Give me name and phone please" тощо.
Декоратор input_error повинен обробляти винятки, що виникають у функціях — 
handler — і це винятки KeyError, ValueError, IndexError. Коли відбувається 
виняток декоратор повинен повертати відповідь користувачеві. 
Виконання програми при цьому не припиняється.

'''

def input_error(func):
    """
    Декоратор обробляє помилки:
    - KeyError
    - ValueError
    - IndexError

    У ВСІХ випадках повертає одне повідомлення:
        "Enter the argument for the command"
    
    Це відповідає прикладу в умові ДЗ.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError):
            return "Enter the argument for the command"
    return wrapper


def parse_input(user_input):
    """
    Розбиваємо рядок на команду та аргументи.
    Повертає:
        command (str)
        args (list[str])
    """
    parts = user_input.split()
    if not parts:
        return "", []
    return parts[0].lower(), parts[1:]


@input_error
def add_contact(args, contacts):
    """
    Додаємо контакт.
    Формат: add <name> <phone>

    Помилки:
        ValueError → якщо мало аргументів
    """
    if len(args) != 2:
        raise ValueError

    name, phone = args
    contacts[name.lower()] = (name, phone)
    return "Contact added."


@input_error
def change_contact(args, contacts):
    """
    Змінюємо номер телефону існуючого контакту.
    Формат: change <name> <phone>

    Помилки:
        ValueError — неправильна кількість аргументів
        KeyError — контакт не існує
    """
    if len(args) != 2:
        raise ValueError

    name, phone = args
    key = name.lower()

    if key not in contacts:
        raise KeyError

    original_name = contacts[key][0]
    contacts[key] = (original_name, phone)
    return "Contact updated."


@input_error
def show_phone(args, contacts):
    """
    Показуємо номер телефону контакту.
    Формат: phone <name>

    Помилки:
        IndexError — не передали ім'я
        KeyError — контакту не існує
    """
    name = args[0]  # може викликати IndexError
    key = name.lower()

    if key not in contacts:
        raise KeyError

    return contacts[key][1]


def show_all(contacts):
    """
    Показуємо всі контакти.
    """
    if not contacts:
        return "No contacts saved."

    sorted_contacts = sorted(contacts.values(), key=lambda x: x[0].lower())
    return "\n".join(f"{name}: {phone}" for name, phone in sorted_contacts)


def main():
    """
    Основна функція запуску консольного бота.

    Реалізує нескінченний цикл обробки команд користувача.
    Приймає текстові команди через input(),
    визначає потрібну дію та викликає відповідні handler-функції.

    Підтримувані команди:
        - hello      → привітання
        - add        → додати новий контакт
        - change     → змінити номер існуючого контакту
        - phone      → показати номер телефону контакту
        - all        → показати всі контакти
        - exit/close → завершити роботу бота

    Усі помилки, пов’язані з некоректним введенням аргументів,
    обробляються за допомогою декоратора input_error,
    що забезпечує стабільність роботи та запобігає завершенню програми.
    """
    contacts = {}
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        command, args = parse_input(user_input)

        if command in ("exit", "close"):
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, contacts))

        elif command == "change":
            print(change_contact(args, contacts))

        elif command == "phone":
            print(show_phone(args, contacts))

        elif command == "all":
            print(show_all(contacts))

        else:
            print("Invalid command. Try again.")


if __name__ == "__main__":
    main()
