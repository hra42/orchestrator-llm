import json
from typing import Dict, List, Tuple


class LLMSelector:
    def __init__(self, model_config_path: str):
        with open(model_config_path, 'r') as f:
            self.model_config = json.load(f)

    def select_llm(self, task_type: str) -> Tuple[str, float]:
        best_model = ""
        best_score = 0.0

        for model, capabilities in self.model_config.items():
            score = capabilities.get(task_type, capabilities.get('general', 0.0))
            if score > best_score:
                best_score = score
                best_model = model

        if not best_model:
            # If no suitable model found, return the first model as a fallback
            best_model = next(iter(self.model_config))
            best_score = self.model_config[best_model].get('general', 0.0)

        return best_model, best_score

    def distribute_tasks(self, tasks: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
        distribution: Dict[str, List[Dict[str, str]]] = {}
        for task in tasks:
            model, _ = self.select_llm(task['task_type'])
            if model not in distribution:
                distribution[model] = []
            distribution[model].append(task)
        return distribution
