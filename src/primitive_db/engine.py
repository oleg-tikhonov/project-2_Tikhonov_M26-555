import prompt


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