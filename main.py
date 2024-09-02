from src.task_generator.abstract_sequence_generator import AbstractSequenceGenerator
from src.evaluator.base_evaluator import BaseEvaluator
from src.models.simple_model import RandomModel


def main():
    # Generate tasks
    generator = AbstractSequenceGenerator()
    tasks = generator.generate(1)  # Generate 1 task for this example

    # Initialize model and evaluator
    model = RandomModel()
    evaluator = BaseEvaluator()

    # Solve tasks and evaluate
    total_score = 0
    for task in tasks:
        prediction = model.solve(task)
        score = evaluator.evaluate(task, prediction)
        total_score += score

        print(f"Task ID: {task.id}")
        print(f"Sequence: {' -> '.join(task.sequence)}")
        print(f"Options: {', '.join(task.options)}")
        print(f"Model's prediction: {prediction}")
        print(f"Correct answer: {task.correct_answer}")
        print(f"Score: {score}")
        print()

    average_score = total_score / len(tasks)
    print(f"Average score: {average_score}")


if __name__ == "__main__":
    main()
