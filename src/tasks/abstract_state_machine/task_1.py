from ...task_base import BaseTask
from ...task_registry import TaskRegistry

import random
from dataclasses import dataclass
from uuid import uuid4
from typing import Dict, List, Tuple
import re


@dataclass
class AbstractStateMachineTask:
    id: str
    states: List[str]
    transitions: Dict[Tuple[str, str], str]
    start_state: str
    input_sequence: List[str]
    options: List[str]
    correct_answer: str
    prompt: str


@TaskRegistry.register("abstract_state_machine_1")
class AbstractStateMachineTask1(BaseTask):
    def __init__(self):
        self.possible_states = ["A", "B", "C", "D", "E"]
        self.possible_inputs = ["0", "1"]

    def create_prompt(
        self, states, transitions, start_state, input_sequence, options
    ) -> str:
        description = "Consider an abstract state machine with the following rules:\n"
        description += f"- The machine starts in state {start_state}\n"
        for (state, input_val), next_state in transitions.items():
            description += f"- If in state {state} and receives '{input_val}', it transitions to state {next_state}\n"

        description += f"\nIf the machine receives the input sequence {' '.join(input_sequence)}, what state will it end up in?"

        prompt = f"{description}\n\n"
        prompt += "Options:\n"
        for i, option in enumerate(options):
            prompt += f"{chr(65+i)}. State {option}\n"

        prompt += "\nPlease respond with the letter corresponding to your answer."
        return prompt

    def generate(self) -> AbstractStateMachineTask:
        task_id = str(uuid4())[:8]

        # Generate states
        num_states = random.randint(3, 5)
        states = self.possible_states[:num_states]

        # Generate transitions
        transitions = {}
        for state in states:
            for input_val in self.possible_inputs:
                transitions[(state, input_val)] = random.choice(states)

        # Generate input sequence
        sequence_length = random.randint(3, 6)
        input_sequence = [
            random.choice(self.possible_inputs) for _ in range(sequence_length)
        ]

        # Calculate correct answer
        start_state = "A"  # Start state
        current_state = start_state
        for input_val in input_sequence:
            current_state = transitions[(current_state, input_val)]

        # Generate options
        options = states.copy()
        random.shuffle(options)

        prompt = self.create_prompt(
            states, transitions, start_state, input_sequence, options
        )

        task = AbstractStateMachineTask(
            id=f"ABS-STATE-{task_id}",
            states=states,
            transitions=transitions,
            start_state=start_state,
            input_sequence=input_sequence,
            options=options,
            correct_answer=current_state,
            prompt=prompt,
        )

        return task

    def evaluate(self, task: AbstractStateMachineTask, prediction: str) -> float:
        correct_index = task.options.index(task.correct_answer)
        correct_letter = chr(65 + correct_index)
        return 1.0 if prediction.upper() == correct_letter else 0.0

    @staticmethod
    def parse_response(response: str) -> str:
        pattern = r"\[([A-E])\]"
        match = re.search(pattern, response, re.IGNORECASE)

        if match:
            return match.group(1).upper()
