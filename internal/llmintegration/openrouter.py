import asyncio
import os
from typing import Any, Dict, List

from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential


class OpenRouterLLMIntegrator:
    def __init__(self):
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY is not set in the environment variables."
            )

        self.client = AsyncOpenAI(
            base_url=os.environ.get(
                "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
            ),
            api_key=api_key,
        )
        self.app_url = os.environ.get("APP_URL", "http://localhost:8501")
        self.app_title = os.environ.get("APP_TITLE", "Orchestrator-LLM")

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def call_llm(self, model: str, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        try:
            completion = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                extra_headers={
                    "HTTP-Referer": self.app_url,
                    "X-Title": self.app_title,
                },
            )
            return {
                "status": "success",
                "response": completion.choices[0].message.content,
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def process_tasks_parallel(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        coroutines = [self.call_llm(task["model"], task["messages"]) for task in tasks]
        results = await asyncio.gather(*coroutines, return_exceptions=True)
        return [{"task": task, **result} for task, result in zip(tasks, results)]

    async def process_tasks_sequential(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for task in tasks:
            result = await self.call_llm(task["model"], task["messages"])
            results.append({"task": task, **result})
            if result["status"] == "error":
                break  # Stop processing if an error occurs
        return results

    async def orchestrate_tasks(self, tasks: List[Dict[str, Any]], parallel: bool = True) -> List[Dict[str, Any]]:
        if parallel:
            return await self.process_tasks_parallel(tasks)
        else:
            return await self.process_tasks_sequential(tasks)


async def run_llm_tasks(tasks: List[Dict[str, Any]], parallel: bool = True) -> List[Dict[str, Any]]:
    integrator = OpenRouterLLMIntegrator()
    return await integrator.orchestrate_tasks(tasks, parallel)
