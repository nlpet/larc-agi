import importlib
import os


def load_all_tasks():
    tasks_dir = os.path.join(os.path.dirname(__file__), "..", "tasks")
    for category in os.listdir(tasks_dir):
        category_dir = os.path.join(tasks_dir, category)
        if os.path.isdir(category_dir):
            for task_file in os.listdir(category_dir):
                if task_file.endswith(".py") and not task_file.startswith("__"):
                    module_name = f"src.tasks.{category}.{task_file[:-3]}"
                    importlib.import_module(module_name)
