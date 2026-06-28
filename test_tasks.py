# test_tasks.py
import pytest
from todo_list.main import add_task, list_tasks, complete_task, delete_task


def test_add_task():
    # Очищаем глобальный список перед тестом
    global tasks
    tasks = []

    task = add_task("Test", "Description", "high")
    assert task["title"] == "Test"
    assert task["completed"] is False
    assert len(tasks) == 1


def test_complete_task():
    pass