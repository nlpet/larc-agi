from dataclasses import dataclass
from typing import List


@dataclass
class Task:
    id: str
    correct_answer: str


@dataclass
class AnalogyTask:
    id: str
    prompt: str
    options: List[str]
    correct_answer: str


@dataclass
class AbstractSequenceTask:
    id: str
    sequence: List[str]
    options: List[str]
    correct_answer: str
