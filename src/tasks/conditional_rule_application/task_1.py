from ...task_base import BaseTask
from ...task_registry import TaskRegistry

import random
from dataclasses import dataclass
from uuid import uuid4
from typing import List, Dict


@dataclass
class ConditionalRuleApplicationTask:
    id: str
    rules: List[str]
    scenario: str
    options: List[str]
    correct_answer: str
    prompt: str


@TaskRegistry.register("conditional_rule_application_1")
class ConditionalRuleApplicationTask1(BaseTask):
    def __init__(self):
        self.concepts = [
            "zoop",
            "flap",
            "morf",
            "glix",
            "plex",
            "yurn",
            "krel",
            "vish",
            "blex",
            "drok",
        ]
        self.rule_templates = [
            "If {A}, then {B}.",
            "If {A} and not {B}, then {C}.",
            "If {A} or {B}, then {C}.",
            "If not {A}, then {B}.",
            "If {A} and {B}, then not {C}.",
        ]

    def create_prompt(self, rules, scenario, options) -> str:
        prompt = "Given the following rules:\n"
        for rule in rules:
            prompt += f"- {rule}\n"
        prompt += f"\nScenario: {scenario}\n\n"
        prompt += "What is the result?\n\n"
        prompt += "Options:\n"
        for i, option in enumerate(options):
            prompt += f"{chr(65+i)}. {option}\n"
        prompt += "\nPlease respond with the letter corresponding to your answer."
        return prompt

    def generate(self) -> ConditionalRuleApplicationTask:
        task_id = str(uuid4())[:8]

        # Generate rules
        used_concepts = random.sample(self.concepts, 5)
        rules = []
        for template in random.sample(self.rule_templates, 3):
            rules.append(
                template.format(
                    A=used_concepts[0], B=used_concepts[1], C=used_concepts[2]
                )
            )

        # Generate scenario
        scenario_concepts = random.sample(used_concepts, random.randint(2, 3))
        scenario = (
            f"Given {', '.join(scenario_concepts[:-1])} and {scenario_concepts[-1]}"
        )

        # Determine correct answer
        correct_answer = random.choice(
            [concept for concept in used_concepts if concept not in scenario_concepts]
        )

        # Generate options
        options = [correct_answer] + random.sample(
            [c for c in self.concepts if c != correct_answer], 3
        )
        random.shuffle(options)

        prompt = self.create_prompt(rules, scenario, options)

        task = ConditionalRuleApplicationTask(
            id=f"COND-RULE-{task_id}",
            rules=rules,
            scenario=scenario,
            options=options,
            correct_answer=correct_answer,
            prompt=prompt,
        )

        return task

    def evaluate(self, task, prediction: str) -> float:
        return 1.0 if prediction == task.correct_answer else 0.0

    @staticmethod
    def parse_response(response: str) -> str:
        response = response.strip().upper()
        if response in ["A", "B", "C", "D"]:
            return response
        for char in response:
            if char in ["A", "B", "C", "D"]:
                return char
        return None
