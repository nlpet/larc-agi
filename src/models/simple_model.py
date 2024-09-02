import random
from ..data_models import Task


class RandomModel:
    def solve(self, task: Task) -> str:
        return random.choice(task.options)
