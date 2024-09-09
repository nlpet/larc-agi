from ...task_base import BaseTask
from ...task_registry import TaskRegistry

import random
from dataclasses import dataclass
from uuid import uuid4
from typing import List, Dict
import re


@dataclass
class PatternExtrapolationTask:
    id: str
    sequence: List[str]
    options: List[str]
    correct_answer: str
    prompt: str


@TaskRegistry.register("pattern_extrapolation_1")
class PatternExtrapolationTask1(BaseTask):
    def __init__(self):
        self.shapes = [
            "circle",
            "square",
            "triangle",
            "star",
            "hexagon",
            "octagon",
            "diamond",
        ]
        self.sizes = ["tiny", "small", "medium", "large", "huge"]
        self.colors = [
            "red",
            "blue",
            "green",
            "yellow",
            "purple",
            "orange",
            "pink",
            "teal",
        ]
        self.transformations = [
            "grows",
            "shrinks",
            "rotates",
            "splits",
            "merges",
            "changes color",
            "inverts",
            "multiplies",
            "transforms",
            "oscillates",
        ]

    def create_prompt(self, sequence, options) -> str:
        prompt = "Analyze the following sequence of shape transformations:\n"
        for step in sequence:
            prompt += f"{step}\n"
        prompt += "\nBased on the pattern, what is the most likely next transformation in this sequence?\n\n"
        prompt += "Options:\n"
        for i, option in enumerate(options):
            prompt += f"[{chr(65+i)}]. {option}\n"
        prompt += "\nPlease respond with the letter corresponding to your answer wrapped in square brackets, e.g. [X]"
        return prompt

    def generate(self) -> PatternExtrapolationTask:
        task_id = str(uuid4())[:8]

        # Generate a complex pattern
        pattern_type = random.choice(
            ["multi_attribute", "nested", "fibonacci", "prime_indexed"]
        )

        print(pattern_type)
        sequence = []
        current_state = {
            "shape": random.choice(self.shapes),
            "size": random.choice(self.sizes),
            "color": random.choice(self.colors),
            "count": 1,
        }

        if pattern_type == "multi_attribute":
            sequence, current_state, correct_next = (
                self.generate_multi_attribute_pattern(current_state)
            )
        elif pattern_type == "nested":
            sequence, current_state, correct_next = self.generate_nested_pattern(
                current_state
            )
        elif pattern_type == "fibonacci":
            sequence, current_state, correct_next = self.generate_fibonacci_pattern(
                current_state
            )
        else:  # prime_indexed
            sequence, current_state, correct_next = self.generate_prime_indexed_pattern(
                current_state
            )

        # Generate options
        options = [correct_next]
        while len(options) < 4:
            fake_option = self.generate_fake_option(current_state)
            if fake_option not in options:
                options.append(fake_option)

        random.shuffle(options)

        prompt = self.create_prompt(sequence, options)

        task = PatternExtrapolationTask(
            id=f"PATTERN-EXTRA-{task_id}",
            sequence=sequence,
            options=options,
            correct_answer=correct_next,
            prompt=prompt,
        )

        return task

    def generate_multi_attribute_pattern(self, initial_state):
        sequence = []
        state = initial_state.copy()
        transformations = random.sample(self.transformations, 3)

        for i in range(5):
            current_transform = transformations[i % 3]
            sequence.append(self.apply_transformation(state, current_transform))

        correct_next = self.apply_transformation(state, transformations[5 % 3])
        return sequence, state, correct_next

    def generate_nested_pattern(self, initial_state):
        sequence = []
        state = initial_state.copy()
        outer_transform = random.choice(self.transformations)
        inner_transform = random.choice(self.transformations)

        for i in range(5):
            if i % 2 == 0:
                sequence.append(self.apply_transformation(state, outer_transform))
            else:
                sequence.append(self.apply_transformation(state, inner_transform))

        correct_next = self.apply_transformation(
            state, outer_transform if len(sequence) % 2 == 0 else inner_transform
        )
        return sequence, state, correct_next

    def generate_fibonacci_pattern(self, initial_state):
        sequence = []
        state = initial_state.copy()
        fib = [1, 1, 2, 3, 5, 8]
        transform = random.choice(self.transformations)

        for i in range(5):
            state["count"] = fib[i]
            sequence.append(self.apply_transformation(state, transform))

        state["count"] = fib[5]
        correct_next = self.apply_transformation(state, transform)
        return sequence, state, correct_next

    def generate_prime_indexed_pattern(self, initial_state):
        sequence = []
        state = initial_state.copy()
        primes = [2, 3, 5, 7, 11]
        transform = random.choice(self.transformations)

        for i in range(1, 6):
            if i in primes:
                sequence.append(self.apply_transformation(state, transform))
            else:
                sequence.append(
                    f"A {state['size']} {state['color']} {state['shape']} remains unchanged."
                )

        correct_next = (
            self.apply_transformation(state, transform)
            if 6 in primes
            else f"A {state['size']} {state['color']} {state['shape']} remains unchanged."
        )
        return sequence, state, correct_next

    def apply_transformation(self, state: Dict[str, str], transformation: str) -> str:
        if transformation == "grows":
            state["size"] = self.sizes[
                min(self.sizes.index(state["size"]) + 1, len(self.sizes) - 1)
            ]
        elif transformation == "shrinks":
            state["size"] = self.sizes[max(self.sizes.index(state["size"]) - 1, 0)]
        elif transformation == "changes color":
            state["color"] = random.choice(
                [c for c in self.colors if c != state["color"]]
            )
        elif transformation == "splits":
            state["count"] *= 2
        elif transformation == "merges":
            state["count"] = max(1, state["count"] // 2)
        elif transformation == "inverts":
            state["shape"] = random.choice(self.shapes)  # Simplified inversion
        elif transformation == "multiplies":
            state["count"] *= 3
        elif transformation == "transforms":
            state["shape"] = random.choice(self.shapes)
        elif transformation == "oscillates":
            state["size"] = random.choice(self.sizes)

        count_str = f"{state['count']} " if state["count"] > 1 else ""
        return f"{count_str}{state['size']} {state['color']} {state['shape']}(s) {transformation}."

    def generate_fake_option(self, current_state):
        fake_state = current_state.copy()
        fake_state["shape"] = random.choice(self.shapes)
        fake_state["size"] = random.choice(self.sizes)
        fake_state["color"] = random.choice(self.colors)
        fake_state["count"] = random.randint(1, 5)
        fake_transform = random.choice(self.transformations)
        return self.apply_transformation(fake_state, fake_transform)

    def evaluate(self, task, prediction: str) -> float:
        return 1.0 if prediction == task.correct_answer else 0.0

    @staticmethod
    def parse_response(response: str) -> str:
        pattern = r"\[([A-E])\]"
        match = re.search(pattern, response, re.IGNORECASE)

        if match:
            return match.group(1).upper()
        return None
