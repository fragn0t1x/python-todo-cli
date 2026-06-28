# test_tasks.py
import pytest
from todo_list.main import tasks, add_task, complete_task, delete_task, search_tasks, list_tasks, sort_tasks, get_all_tasks


# Фикстура для очистки списка задач перед каждым тестом
@pytest.fixture
def clean_tasks():
    tasks.clear()
    yield
    tasks.clear()


# --- Тесты для add_task ---
def test_add_task(clean_tasks):
    task = add_task("Купить хлеб", "Бездрожжевой", "high")
    assert task["title"] == "Купить хлеб"
    assert task["description"] == "Бездрожжевой"
    assert task["priority"] == "high"
    assert task["completed"] is False
    assert len(tasks) == 1
    assert tasks[0]["id"] == 1


def test_add_task_default_priority(clean_tasks):
    task = add_task("Просто задача")
    assert task["priority"] == "medium"
    assert task["description"] == ""


# --- Тесты для complete_task ---
def test_complete_task(clean_tasks):
    add_task("Задача")
    completed_task = complete_task(1)
    assert completed_task is not None
    assert completed_task["completed"] is True
    assert tasks[0]["completed"] is True


def test_complete_task_not_found(clean_tasks):
    add_task("Задача")
    result = complete_task(999)
    assert result is None


# --- Тесты для delete_task ---
def test_delete_task(clean_tasks):
    add_task("Задача 1")
    add_task("Задача 2")
    assert delete_task(1) is True
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Задача 2"

    assert delete_task(999) is False


# --- Тесты для search_tasks ---
def test_search_tasks(clean_tasks):
    add_task("Купить молоко", "Купить в магазине")
    add_task("Позвонить маме", "Вечером")

    results = search_tasks("молоко")
    assert len(results) == 1
    assert results[0]["title"] == "Купить молоко"

    results = search_tasks("не существует")
    assert results == []


# --- Тесты для list_tasks ---
def test_list_tasks(clean_tasks):
    add_task("Активная задача")
    add_task("Завершенная задача")
    complete_task(2)

    # Активные задачи
    active = list_tasks(show_completed=False)
    assert len(active) == 1
    assert active[0]["title"] == "Активная задача"

    # Выполненные задачи
    completed = list_tasks(show_completed=True)
    assert len(completed) == 1
    assert completed[0]["title"] == "Завершенная задача"

    # Все задачи (новая функция)
    all_tasks = get_all_tasks()
    assert len(all_tasks) == 2


def test_sort_tasks(clean_tasks):
    """Проверяет сортировку задач по приоритету."""
    add_task("Низкий приоритет", priority="low")
    add_task("Высокий приоритет", priority="high")
    add_task("Средний приоритет", priority="medium")

    sorted_tasks = sort_tasks(by="priority")

    assert sorted_tasks[0]["priority"] == "high"
    assert sorted_tasks[1]["priority"] == "medium"
    assert sorted_tasks[2]["priority"] == "low"