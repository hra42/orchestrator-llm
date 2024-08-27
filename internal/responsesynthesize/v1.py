from collections import defaultdict
from typing import Any, Dict, List


class ResponseSynthesizer:
    def __init__(self, nlp_model):
        self.nlp_model = nlp_model  # Pre-trained NLP model for text analysis

    def collect_responses(
        self, llm_outputs: List[Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """
        Collect and organize responses from multiple LLMs.
        """
        organized_responses = defaultdict(list)
        for output in llm_outputs:
            task_type = output["task"]["task_type"]
            response = output["response"]
            organized_responses[task_type].append(response)
        return organized_responses

    def analyze_sentiment(self, text: str) -> float:
        """
        Analyze the sentiment of a given text using the NLP model.
        """
        return self.nlp_model.analyze_sentiment(text)

    def extract_key_points(self, text: str) -> List[str]:
        """
        Extract key points from a given text using the NLP model.
        """
        return self.nlp_model.extract_key_points(text)

    def synthesize_responses(self, organized_responses: Dict[str, List[str]]) -> str:
        """
        Synthesize collected responses into a coherent output.
        """
        synthesized_output = ""
        for task_type, responses in organized_responses.items():
            synthesized_output += f"\n## {task_type.capitalize()}\n"

            if task_type in ["summarize", "analyze"]:
                # For summary and analysis, combine key points
                all_key_points = []
                for response in responses:
                    all_key_points.extend(self.extract_key_points(response))
                synthesized_output += "\n".join(
                    set(all_key_points)
                )  # Remove duplicates

            elif task_type == "generate":
                # For generated content, select based on sentiment or use the longest
                best_response = max(
                    responses, key=lambda x: (self.analyze_sentiment(x), len(x))
                )
                synthesized_output += best_response

            elif task_type == "translate":
                # For translations, present all versions
                for i, response in enumerate(responses, 1):
                    synthesized_output += f"Version {i}: {response}\n"

            elif task_type == "classify":
                # For classification, use majority voting
                classifications = [r.strip().lower() for r in responses]
                most_common = max(set(classifications), key=classifications.count)
                synthesized_output += f"Majority Classification: {most_common}\n"

            else:  # General knowledge or other types
                # Combine unique information from all responses
                combined_info = set()
                for response in responses:
                    combined_info.update(self.extract_key_points(response))
                synthesized_output += "\n".join(combined_info)

        return synthesized_output

    def process_llm_outputs(self, llm_outputs: List[Dict[str, Any]]) -> str:
        """
        Main method to process LLM outputs and produce a synthesized response.
        """
        organized_responses = self.collect_responses(llm_outputs)
        return self.synthesize_responses(organized_responses)
