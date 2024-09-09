from ...task_base import BaseTask
from ...task_registry import TaskRegistry

import random
import string
from dataclasses import dataclass
from uuid import uuid4

from typing import List, Dict, Union
import re


@dataclass
class LogicalGridPuzzleTask:
    id: str
    entities: Dict[str, List[str]]
    clues: List[str]
    question: str
    options: List[str]
    correct_answer: str
    prompt: str


@TaskRegistry.register("logical_grid_puzzle_1")
class LogicalGridPuzzleTask1(BaseTask):
    def __init__(self):
        self.categories = {
            "names": ["Alice", "Bob", "Charlie", "David", "Eva"],
            "pets": ["dog", "cat", "fish", "bird", "hamster"],
            "colors": ["red", "blue", "green", "yellow", "purple"],
            "fruits": ["apple", "banana", "orange", "grape", "pear"],
            "sports": ["soccer", "tennis", "swimming", "basketball", "running"],
        }

    def generate_clues(self, categories, solution, entities):
        clues = []
        for _ in range(4):  # Generate 4 clues
            cat1, cat2 = random.sample(categories, 2)
            item1 = random.choice(entities[cat1])
            item2 = next(item for item in solution if item1 in item)
            item2 = next(x for x in item2 if x in entities[cat2])
            clues.append(f"The {cat1} {item1} is associated with the {cat2} {item2}.")
        return clues

    def create_prompt(self, entities, question, clues, options) -> str:
        description = "Given the following information:\n"
        for category, items in entities.items():
            description += f"{category.capitalize()}: {', '.join(items)}\n"
        description += "\nClues:\n"
        for clue in clues:
            description += f"- {clue}\n"
        description += f"\n{question}"

        prompt = f"{description}\n\n"
        prompt += "Options:\n"
        for i, option in enumerate(options):
            prompt += f"[{chr(65+i)}]. {option}\n"

        prompt += "\nPlease respond with the letter corresponding to your answer."
        return prompt

    def generate(self) -> LogicalGridPuzzleTask:
        task_id = str(uuid4())[:8]

        selected_categories = random.sample(list(self.categories.keys()), 3)
        entities = {
            cat: random.sample(self.categories[cat], 3) for cat in selected_categories
        }

        # Create a random solution
        solution = list(zip(*[entities[cat] for cat in selected_categories]))
        random.shuffle(solution)

        # Generate clues
        clues = self.generate_clues(selected_categories, solution, entities)

        # Generate question and options
        question_category = random.choice(selected_categories)
        question_entity = random.choice(entities[question_category])
        correct_answer = next(item for item in solution if question_entity in item)
        answer_category = random.choice(
            [cat for cat in selected_categories if cat != question_category]
        )
        correct_answer = next(
            x for x in correct_answer if x in entities[answer_category]
        )

        options = entities[answer_category].copy()
        random.shuffle(options)

        question = f"What {answer_category} is associated with the {question_category} {question_entity}?"

        prompt = self.create_prompt(entities, question, clues, options)

        task = LogicalGridPuzzleTask(
            id=f"GRID-PUZZLE-{task_id}",
            entities=entities,
            clues=clues,
            question=question,
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
