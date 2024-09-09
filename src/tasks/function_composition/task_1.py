from ...task_base import BaseTask
from ...task_registry import TaskRegistry

import random
from dataclasses import dataclass
from uuid import uuid4
from typing import List, Dict, Callable
import re
import math


@dataclass
class FunctionCompositionTask:
    id: str
    function_definitions: Dict[str, str]
    composition: List[str]
    input_value: float
    options: List[float]
    correct_answer: float
    prompt: str


@TaskRegistry.register("function_composition_1")
class FunctionCompositionTask1(BaseTask):
    def __init__(self):
        self.functions = {
            "double": ("f(x) = 2x", lambda x: 2 * x),
            "add_one": ("f(x) = x + 1", lambda x: x + 1),
            "square": ("f(x) = x^2", lambda x: x**2),
            "half": ("f(x) = x / 2", lambda x: x / 2),
            "triple": ("f(x) = 3x", lambda x: 3 * x),
            "subtract_two": ("f(x) = x - 2", lambda x: x - 2),
            "reciprocal": ("f(x) = 1/x", lambda x: 1 / x if x != 0 else float("inf")),
            "abs": ("f(x) = |x|", abs),
            "sin": ("f(x) = sin(x)", math.sin),
            "cos": ("f(x) = cos(x)", math.cos),
            "log": ("f(x) = log(x)", lambda x: math.log(x) if x > 0 else float("nan")),
            "exp": ("f(x) = e^x", math.exp),
            "floor": ("f(x) = ⌊x⌋", math.floor),
            "ceil": ("f(x) = ⌈x⌉", math.ceil),
            "cube": ("f(x) = x^3", lambda x: x**3),
            "sqrt": ("f(x) = √x", lambda x: math.sqrt(x) if x >= 0 else float("nan")),
        }

    def create_prompt(self, composition, input_value, options, function_defs) -> str:
        description = "Given the following functions:\n"
        for f, def_ in function_defs.items():
            description += f"{f}: {def_}\n"
        description += (
            f"\nCompose these functions in the order: {' -> '.join(composition)}\n"
        )
        description += f"What is the result when the input is {input_value}? (Round your answer to 3 decimal places)"

        prompt = f"{description}\n\n"
        prompt += "Options:\n"
        for i, option in enumerate(options):
            prompt += f"[{chr(65+i)}]. {option:.3f}\n"

        prompt += "\nPlease respond with the letter corresponding to your answer wrapped in square brackets, e.g. [X]"
        return prompt

    def generate(self) -> FunctionCompositionTask:
        task_id = str(uuid4())[:8]

        # Select 3-5 functions for composition
        composition = random.sample(list(self.functions.keys()), random.randint(3, 5))

        # Generate input value (now including negative and decimal numbers)
        input_value = round(random.uniform(-10, 10), 2)

        # Calculate correct answer
        result = input_value
        for func in composition:
            result = self.functions[func][1](result)

        # Round the result to 3 decimal places
        result = round(result, 3)

        # Generate options
        options = [result]
        i = 0
        while len(options) < 4:
            fake_option = self.generate_fake_option(result)
            if fake_option not in options:
                options.append(fake_option)

        random.shuffle(options)

        function_defs = {f: self.functions[f][0] for f in composition}
        prompt = self.create_prompt(composition, input_value, options, function_defs)

        task = FunctionCompositionTask(
            id=f"FUNC-COMP-{task_id}",
            function_definitions=function_defs,
            composition=composition,
            input_value=input_value,
            options=options,
            correct_answer=result,
            prompt=prompt,
        )

        return task

    def generate_fake_option(self, correct_result: float) -> float:
        # Generate a fake option that's close to the correct result
        deviation = random.uniform(0.1, 2.0)
        fake_option = correct_result + (random.choice([-1, 1]) * deviation)
        return round(fake_option, 3)

    def evaluate(self, task, prediction: str) -> float:
        correct_index = task.options.index(task.correct_answer)
        correct_letter = chr(65 + correct_index)
        return 1.0 if prediction.upper() == correct_letter else 0.0

    @staticmethod
    def parse_response(response: str) -> str:
        pattern = r"\[([A-E])\]"
        match = re.search(pattern, response, re.IGNORECASE)

        if match:
            return match.group(1).upper()
        return None
