import json

FILENAME = "tasks.json"
def save_tasks():
    """Сохраняет список задач в JSON-файл."""
    try:
        with open(FILENAME, "w", encoding="utf-8") as file:
            # indent=4 делает файл читаемым для человека
            json.dump(tasks, file, ensure_ascii=False, indent=4)
        print("Задачи успешно сохранены!")
    except IOError:
        print("Ошибка: не удалось сохранить задачи в файл.")


def load_tasks():
    """Загружает список задач из JSON-файла. Возвращает пустой список, если файла нет."""
    try:
        with open(FILENAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        # Если файла еще нет (первый запуск), возвращаем пустой список
        return []
    except json.JSONDecodeError:
        print("Ошибка: файл поврежден. Создан новый список задач.")
        return []

tasks = load_tasks()

def add_task(title: str, description: str = "", priority: str = "medium") -> dict | None:
    """Добавляет новую задачу"""
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "completed": False,
        "priority": priority
    }
    tasks.append(task)
    return task


def list_tasks(show_completed:bool = False) -> list[dict]:
    """Возвращает задачи(так же по условию)"""
    if show_completed:
        return [task for task in tasks if task["completed"]]
    return [task for task in tasks if not task["completed"]]


def complete_task(task_id: int) -> dict | None:
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return task
    return None  # Задача не найдена

def delete_task(task_id: int) -> bool:
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return True
    return False

def search_tasks(keyword: str) -> list[dict] | None:
    """Находит задачи по ключевому слову"""
    keyword = keyword.lower()
    tasks_found = [task for task in tasks if keyword in task["title"].lower() or keyword in task["description"].lower()]
    if tasks_found is None:
        return None
    return tasks_found

def sort_tasks(by: str = "priority") -> list[dict] | None:
    """Сортирует задачи по приоритету или по дате добавления"""
    if by == "priority":
        high_tasks = [task for task in tasks if task["priority"] == "high"]
        medium_tasks = [task for task in tasks if task["priority"] == "medium"]
        low_tasks = [task for task in tasks if task["priority"] == "low"]
        return high_tasks+medium_tasks+low_tasks
    else:
        return tasks[::-1]



def main():
    while True:
        print("Выбери команду:\n\t1)Добавить задачу\n\t2)Получить список задач\n\t3)Отметить задачу завершенной\n\t4)Удалить задачу\n\t5)Найти задачи по ключевому слову\n\t6)Отсортировать задачи\n\t7)Закрыть программу")
        num_command = int(input("Введи номер команды: "))
        match num_command:
            case 1:
                while True:
                    task_title = str(input("Название задачи: "))
                    if task_title == "":
                        print("Имя задачи не должно быть пустым")
                        continue
                    task_description = str(input("Описание задачи(не обязательно):"))
                    task_priority = int(input("Приоритет задачи(не обязательно):\n\t1)Высокий\n\t2)Средний\n\t3)Низкий\n"))
                    match task_priority:
                        case 1:
                            task_priority = "high"
                        case 2:
                            task_priority = "medium"
                        case 3:
                            task_priority = "low"

                    if task_description != "" and task_priority != "":
                        result = add_task(task_title, task_description, task_priority)
                    elif task_description != "" and task_priority == "":
                        result = add_task(task_title, task_description)
                    elif task_description == "" and task_priority != "":
                        result = add_task(task_title, task_priority)
                    elif task_description == "" and task_priority == "":
                        result = add_task(task_title)
                    else:
                        print("Ошибка")
                        continue
                    print(f"Задача {result["id"]}-{result["title"]} успешно добавлена")
                    break


            case 2:
                while True:
                    print("Получить список задач:\n\t1)Всех\n\t2)Завершенных")
                    num_command = int(input("Выбери цифру: "))
                    match num_command:
                        case 1:
                            print(list_tasks())
                            break
                        case 2:
                            print(list_tasks(show_completed=True))
                            break
                        case _:
                            print("нет такого числа")

            case 3:
                while True:
                    task_id = int(input("Введи номер задачи: "))
                    if task_id != "":
                        print(complete_task(task_id))
                        break

            case 4:
                while True:
                    task_id = int(input("Введи номер задачи: "))
                    if task_id != "":
                        print(delete_task(task_id))
                        break
            case 5:
                while True:
                    task_keyword = str(input("Введи ключевое слово: "))
                    if task_keyword != "":
                        print(search_tasks(task_keyword))
                        break
            case 6:
                while True:
                    print("Отсортировать:\n\t1)По важности\n\t2)По дате добавления")
                    num_command = int(input("Введи номер команды: "))
                    match num_command:
                        case 1:
                            print(sort_tasks())
                            break
                        case 2:
                            print(sort_tasks(by="date"))
                            break
                        case _:
                            continue
            case 7:
                save_tasks()
                exit()
            case _:
                print("Нет такой команды, введи снова")


if __name__ == '__main__':
    main()