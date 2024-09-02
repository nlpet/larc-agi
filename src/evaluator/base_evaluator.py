from typing import Tuple
from ..data_models import Task


class BaseEvaluator:
    def evaluate(self, task: Task, prediction: str) -> float:
        return 1.0 if prediction == task.correct_answer else 0.0
