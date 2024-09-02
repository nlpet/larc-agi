from typing import List
from ..data_models import AbstractSequenceTask


class AbstractSequenceGenerator:
    def generate(self, n: int) -> List[AbstractSequenceTask]:
        # In a real implementation, this would generate diverse tasks
        return [
            AbstractSequenceTask(
                id="SEQUENCE-001",
                sequence=["Dog", "Puppy", "Cat", "Kitten", "Horse"],
                options=["Foal", "Colt", "Mare", "Stallion"],
                correct_answer="Foal",
            )
        ]
