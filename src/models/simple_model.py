import random


class RandomModel:
    def solve(self, task) -> str:
        idx = random.choice(range(len(task.options)))
        return chr(65 + idx)
