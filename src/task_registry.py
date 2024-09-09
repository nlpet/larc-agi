from typing import Dict, Type
from .task_base import BaseTask


class TaskRegistry:
    _tasks: Dict[str, Type[BaseTask]] = {}

    @classmethod
    def register(cls, task_name: str):
        def decorator(task_class: Type[BaseTask]):
            cls._tasks[task_name] = task_class
            return task_class

        return decorator

    @classmethod
    def get_task(cls, task_name: str) -> Type[BaseTask]:
        return cls._tasks.get(task_name)

    @classmethod
    def get_all_tasks(cls) -> Dict[str, Type[BaseTask]]:
        return cls._tasks
