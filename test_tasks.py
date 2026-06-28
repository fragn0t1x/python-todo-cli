import pytest
from main import tasks, add_task, complete_task, delete_task, search_tasks, list_tasks


# Фикстура — автоматически очищает список перед каждым тестом
@pytest.fixture
def clean_tasks():
    tasks.clear()
    yield  # Здесь выполняется тест
    tasks.clear()  # После теста опять очищаем


def test_add_task(clean_tasks):
    task = add_task("Тест", "Описание", "high")
    assert task["title"] == "Тест"
    assert task["description"] == "Описание"
    assert task["priority"] == "high"
    assert task["completed"] is False
    assert len(tasks) == 1


def test_complete_task(clean_tasks):
    add_task("Задача")
    task = complete_task(1)
    assert task is not None
    assert task["completed"] is True
    assert tasks[0]["completed"] is True


def test_complete_task_not_found(clean_tasks):
    add_task("Задача")
    result = complete_task(999)
    assert result is None


def test_delete_task(clean_tasks):
    add_task("Задача 1")
    add_task("Задача 2")
    assert delete_task(1) is True
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Задача 2"
    assert delete_task(999) is False


def test_search_tasks(clean_tasks):
    add_task("Купить молоко", "Купить в магазине")
    add_task("Позвонить маме", "Вечером")
    results = search_tasks("молоко")
    assert len(results) == 1
    assert results[0]["title"] == "Купить молоко"

    results = search_tasks("не существует")
    assert results == []  # Пустой список


def test_list_tasks(clean_tasks):
    add_task("Активная задача")
    add_task("Завершенная задача")
    complete_task(2)

    active = list_tasks(show_completed=False)
    assert len(active) == 1
    assert active[0]["title"] == "Активная задача"

    all_tasks = list_tasks(show_completed=True)
    assert len(all_tasks) == 2