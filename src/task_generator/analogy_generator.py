from typing import List
from ..data_models import AnalogyTask


class AnalogyGenerator:
    def generate(self, n: int) -> List[AnalogyTask]:
        return [
            AnalogyTask(
                id="ANALOGY-001",
                prompt="BIRD is to SKY as FISH is to:",
                options=["WATER", "LAND", "AIR", "FOREST"],
                correct_answer="WATER",
            )
        ]
