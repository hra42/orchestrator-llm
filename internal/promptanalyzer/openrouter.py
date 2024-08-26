import json
import os
import re
from typing import Dict, List

import streamlit as st
from openai import OpenAI


class OpenRouterPromptAnalyzer:
    def __init__(self):
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            st.error("OPENROUTER_API_KEY is not set in the environment variables.")
            st.stop()

        self.client = OpenAI(
            base_url=os.environ.get(
                "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
            ),
            api_key=api_key,
        )
        self.app_url = os.environ.get("APP_URL", "https://example.com")
        self.app_title = os.environ.get("APP_TITLE", "Orchestrator-LLM")

    def analyze_prompt(
        self, prompt: str, model: str = "anthropic/claude-3-haiku-20240307"
    ) -> List[Dict[str, str]]:
        system_prompt = """Analyze the given prompt and break it down into sub-prompts. For each sub-prompt, determine the task type, extract key entities and keywords. Respond with a JSON array of objects containing:
        - text: The sub-prompt text
        - task_type: The type of task (e.g., summarize, analyze, generate, translate, classify, or general)
        - entities: A list of key entities mentioned
        - keywords: A list of important keywords
        Ensure your response is valid JSON without any prefixed text."""

        try:
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": self.app_url,
                    "X-Title": self.app_title,
                },
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this prompt:\n\n{prompt}"},
                ],
            )
            content = completion.choices[0].message.content

            # Extract JSON content from the response
            json_content = re.search(r"\[.*\]", content, re.DOTALL)
            if json_content:
                parsed_content = json.loads(json_content.group())
                return parsed_content
            else:
                st.error("No valid JSON found in the response")
                return []
        except json.JSONDecodeError as e:
            st.error(f"Error parsing JSON response: {e}")
            st.write("Raw response content:", content)
            return []
        except Exception as e:
            st.error(f"Error in analyzing prompt: {str(e)}")
            return []

    def get_task_distribution(
        self, sub_prompts: List[Dict[str, str]]
    ) -> Dict[str, int]:
        task_counts = {}
        for sub_prompt in sub_prompts:
            task_type = sub_prompt.get("task_type", "general")
            task_counts[task_type] = task_counts.get(task_type, 0) + 1
        return task_counts
