# test_tasks.py
from todo_list.main import tasks, add_task, complete_task, delete_task


def test_add_task():
    # 1. Подготовка (setup) — очищаем список перед тестом
    tasks.clear()

    # 2. Действие (action) — вызываем функцию
    task = add_task("Купить хлеб", "Бездрожжевой", "high")

    # 3. Проверка (assert) — сравниваем ожидание с реальностью
    assert task["title"] == "Купить хлеб"
    assert task["description"] == "Бездрожжевой"
    assert task["priority"] == "high"
    assert task["completed"] is False
    assert len(tasks) == 1
    assert tasks[0]["id"] == 1


def test_complete_task():
    tasks.clear()
    add_task("Помыть посуду")

    # Выполняем задачу
    completed_task = complete_task(1)

    # Проверяем
    assert completed_task is not None
    assert completed_task["completed"] is True
    assert tasks[0]["completed"] is True


def test_complete_task_not_found():
    tasks.clear()
    add_task("Помыть посуду")

    # Пытаемся выполнить несуществующую задачу
    result = complete_task(999)
    assert result is None


def test_delete_task():
    tasks.clear()
    add_task("Задача 1")
    add_task("Задача 2")

    # Удаляем первую
    result = delete_task(1)
    assert result is True
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Задача 2"

    # Пытаемся удалить несуществующую
    result = delete_task(999)
    assert result is False