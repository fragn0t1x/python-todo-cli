import json
from datetime import datetime

FILENAME = "tasks.json"


def save_tasks():
    """Сохраняет список задач в JSON-файл."""
    try:
        with open(FILENAME, "w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=4)
        print("✅ Задачи сохранены!")
    except IOError:
        print("❌ Ошибка: не удалось сохранить задачи.")


def load_tasks():
    """Загружает список задач из JSON-файла."""
    try:
        with open(FILENAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("❌ Файл поврежден. Создан новый список.")
        return []


tasks = load_tasks()


def add_task(title: str, description: str = "", priority: str = "medium") -> dict:
    """Добавляет новую задачу."""
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "completed": False,
        "priority": priority,
        "created_at": datetime.now().isoformat()
    }
    tasks.append(task)
    return task


def list_tasks(show_completed: bool = False) -> list[dict]:
    """Возвращает задачи. Если show_completed=False — только активные."""
    if show_completed:
        return [task for task in tasks if task["completed"]]
    # Возвращаем только НЕвыполненные задачи
    return [task for task in tasks if not task["completed"]]


def complete_task(task_id: int) -> dict | None:
    """Отмечает задачу как выполненную."""
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return task
    return None


def delete_task(task_id: int) -> bool:
    """Удаляет задачу по ID."""
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return True
    return False


def search_tasks(keyword: str) -> list[dict]:
    """Ищет задачи по ключевому слову."""
    keyword = keyword.lower()
    return [task for task in tasks
            if keyword in task["title"].lower()
            or keyword in task["description"].lower()]


def sort_tasks(by: str = "priority") -> list[dict]:
    """Сортирует задачи по приоритету или дате создания."""
    if by == "priority":
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda t: priority_order.get(t.get("priority", "medium"), 1))
    else:  # by == "date"
        return sorted(tasks, key=lambda t: t.get("created_at", ""), reverse=True)


def get_all_tasks() -> list[dict]:
    """Возвращает все задачи (без фильтрации)."""
    return tasks.copy()

def get_stats() -> dict:
    """Возвращает статистику по задачам."""
    completed = sum(1 for task in tasks if task["completed"])
    by_priority = {"high": 0, "medium": 0, "low": 0}
    for task in tasks:
        priority = task.get("priority", "medium")
        if priority in by_priority:
            by_priority[priority] += 1
    return {
        "total": len(tasks),
        "completed": completed,
        "active": len(tasks) - completed,
        "by_priority": by_priority
    }


def print_task(task: dict) -> None:
    """Красиво выводит задачу."""
    status = "✅" if task["completed"] else "⏳"
    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    priority = task.get("priority", "medium")
    print(f"{task['id']}. {status} {task['title']} "
          f"{priority_emoji.get(priority, '🟡')} ({priority})")
    if task["description"]:
        print(f"   📝 {task['description']}")


def main():
    while True:
        print("\n" + "=" * 40)
        print("📋 МЕНЕДЖЕР ЗАДАЧ")
        print("=" * 40)
        print("1. Добавить задачу")
        print("2. Список задач")
        print("3. Отметить как выполненную")
        print("4. Удалить задачу")
        print("5. Поиск")
        print("6. Сортировка")
        print("7. Статистика")
        print("8. Выход")
        print("=" * 40)

        try:
            choice = int(input("Выбери команду: "))
        except ValueError:
            print("❌ Введи число!")
            continue

        if choice == 1:
            title = input("Название: ").strip()
            if not title:
                print("❌ Название не может быть пустым!")
                continue

            description = input("Описание (необязательно): ").strip()

            print("Приоритет:")
            print("1. 🔴 Высокий")
            print("2. 🟡 Средний")
            print("3. 🟢 Низкий")
            priority_choice = input("Выбери (1-3, Enter = Средний): ").strip()

            priority_map = {"1": "high", "2": "medium", "3": "low"}
            priority = priority_map.get(priority_choice, "medium")

            task = add_task(title, description, priority)
            print(f"✅ Задача {task['id']} добавлена!")

        elif choice == 2:
            print("\n1. Активные задачи")
            print("2. Все задачи")
            sub = input("Выбери (1-2): ").strip()
            show_all = sub == "2"

            tasks_list = list_tasks(show_completed=show_all)
            if not tasks_list:
                print("📭 Нет задач для отображения.")
            else:
                print("\n" + "-" * 40)
                for task in tasks_list:
                    print_task(task)
                print("-" * 40)

        elif choice == 3:
            try:
                task_id = int(input("ID задачи: "))
                task = complete_task(task_id)
                if task:
                    print(f"✅ Задача '{task['title']}' выполнена!")
                else:
                    print("❌ Задача не найдена.")
            except ValueError:
                print("❌ Введи число!")

        elif choice == 4:
            try:
                task_id = int(input("ID задачи: "))
                if delete_task(task_id):
                    print("✅ Задача удалена!")
                else:
                    print("❌ Задача не найдена.")
            except ValueError:
                print("❌ Введи число!")

        elif choice == 5:
            keyword = input("Ключевое слово: ").strip()
            if not keyword:
                print("❌ Введи слово для поиска!")
                continue
            found = search_tasks(keyword)
            if not found:
                print("🔍 Ничего не найдено.")
            else:
                print(f"\n🔍 Найдено {len(found)} задач:")
                for task in found:
                    print_task(task)

        elif choice == 6:
            print("1. По приоритету")
            print("2. По дате создания")
            sub = input("Выбери (1-2): ").strip()
            sort_by = "priority" if sub == "1" else "date"
            sorted_tasks = sort_tasks(by=sort_by)
            print("\n" + "-" * 40)
            for task in sorted_tasks:
                print_task(task)
            print("-" * 40)

        elif choice == 7:
            stats = get_stats()
            print("\n📊 СТАТИСТИКА")
            print("-" * 40)
            print(f"Всего задач: {stats['total']}")
            print(f"✅ Выполнено: {stats['completed']}")
            print(f"⏳ Активных: {stats['active']}")
            print("\nПо приоритетам:")
            for priority, count in stats['by_priority'].items():
                emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                print(f"  {emoji.get(priority, '')} {priority}: {count}")
            print("-" * 40)

        elif choice == 8:
            save_tasks()
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверная команда!")


if __name__ == "__main__":
    main()