from src.utils.task_loader import load_all_tasks
from src.task_registry import TaskRegistry
from src.models.simple_model import RandomModel
from src.models.openai_model import OpenAIModel


def main():
    load_all_tasks()

    model = RandomModel()
    llm = OpenAIModel()

    scores = {"model": 0, "random": 0}

    all_tasks = TaskRegistry.get_all_tasks()

    # Filter on task
    # all_tasks = {k: v for k, v in all_tasks.items() if k == "function_composition_1"}

    for task_name, task_class in all_tasks.items():
        task_cls = task_class()
        task = task_cls.generate()

        llm_response = llm.solve_dummy(task.prompt)
        prediction_llm = task_cls.parse_response(llm_response)

        prediction_rand = model.solve(task)

        scores["random"] += task_cls.evaluate(task, prediction_rand)
        scores["model"] += task_cls.evaluate(task, prediction_llm)

        print(f"Task: {task_name}")
        print(f"LLM Prediction: {prediction_llm}")
        print(f"Random Prediction: {prediction_rand}")
        print(f"LLM Score: {scores['model']}")
        print(f"Task Definition: {task}")
        print()
        print(f"Prompt: {task.prompt}")
        print("- - " * 15)


if __name__ == "__main__":
    main()
