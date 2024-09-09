from ...task_base import BaseTask
from ...task_registry import TaskRegistry

import random
import string
from dataclasses import dataclass
from uuid import uuid4

from typing import List, Dict, Union
import re


@dataclass
class SymbolManipulationTask:
    id: str
    sequence: List[str]
    options: List[str]
    correct_answer: str
    prompt: str


@TaskRegistry.register("symbol_manipulation_1")
class SymbolManipulationTask1(BaseTask):
    def __init__(self):
        self.letters = string.ascii_uppercase
        self.numbers = string.digits[1:]

    def generate_sequence(self, length: int) -> List[str]:
        sequence = []
        for i in range(length):
            letter = self.letters[i % 3]  # Cycle through first 3 letters
            number = self.numbers[(i // 3) % len(self.numbers)]
            sequence.append(f"{letter}{number}")
        return sequence

    def create_prompt(self, sequence, options) -> str:
        formatted_seq = ", ".join(sequence)
        description = f"Given the sequence: {formatted_seq}, what comes next?"
        prompt = f"{description}\n\n"
        prompt += "Options:\n"
        for i, option in enumerate(options):
            prompt += f"[{chr(65+i)}]. {option}\n"

        prompt += "\nPlease respond with the letter corresponding to your answer."
        return prompt

    def generate(self) -> SymbolManipulationTask:
        task_id = str(uuid4())[:8]
        sequence = self.generate_sequence(7)
        correct_answer = (
            f"{self.letters[1 % 3]}{self.numbers[(7 // 3) % len(self.numbers)]}"
        )
        options = [correct_answer] + [
            f"{random.choice(self.letters)}{random.choice(self.numbers)}"
            for _ in range(4)
        ]

        random.shuffle(options)

        prompt = self.create_prompt(sequence, options)

        task = SymbolManipulationTask(
            id=f"SYMBOL-001-{task_id}",
            sequence=sequence,
            options=options,
            correct_answer=correct_answer,
            prompt=prompt,
        )

        return task

    def evaluate(self, task, prediction: str) -> float:
        return 1.0 if prediction == task.correct_answer else 0.0

    @staticmethod
    def parse_response(response: str) -> str:
        pattern = r"\[([A-E])\]"
        match = re.search(pattern, response, re.IGNORECASE)

        if match:
            return match.group(1).upper()
        return None
