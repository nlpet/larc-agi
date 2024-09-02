# Language-based Abstraction and Reasoning Corpus for Artificial General Intelligence (LARC-AGI)

## Overview

The Language-based Abstraction and Reasoning Corpus (LARC-AGI) is a project aimed at creating a linguistic equivalent to François Chollet's Abstraction and Reasoning Corpus (ARC) challenge. This repository is modeled after the [ARC-AGI](https://github.com/fchollet/ARC-AGI) challenge. Please refer to the original repository for more information about the ARC challenge.

The goal of this language-based ARC challenge is to provide a benchmark for measuring machine intelligence in the domain of natural language processing and understanding and to delineate the boundaries between genuine reasoning and memorisation.

## Key Features

- **Few-shot learning**: Tasks are designed to be solvable with minimal examples, testing a system's ability to generalize quickly.
- **Focus on abstraction and reasoning**: Tasks require understanding and manipulating abstract concepts in language.
- **Diverse task types**: Includes a variety of linguistic challenges, from analogical reasoning to pattern recognition in text.
- **Generalization measurement**: Evaluates a system's ability to solve novel, unseen task types.

## Project Structure

```
project_root/
├── src/
│   ├── task_generator/
│   ├── evaluator/
│   ├── models/
│   └── utils/
├── data/
├── tests/
├── notebooks/
├── requirements.txt
└── main.py
```

- `src/`: Contains the core components of the project.
- `data/`: Stores datasets for training, evaluation, and testing.
- `tests/`: Unit tests for various components.
- `notebooks/`: Jupyter notebooks for task exploration and result analysis.

## Getting Started

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/nlpet/larc-agi
   cd larg-agi
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Running the Project

To generate tasks, run a model, and evaluate results:

```
python main.py
```