import asyncio

import streamlit as st

from internal.llmintegration.openrouter import run_llm_tasks
from internal.llmselector.v1 import LLMSelector
from internal.promptanalyzer.openrouter import OpenRouterPromptAnalyzer


async def synthesize_responses(results, synthesis_model):
    # Prepare the prompt for synthesis
    synthesis_prompt = "Synthesize the following responses into a coherent summary:\n\n"
    for result in results:
        synthesis_prompt += f"Task Type: {result['task']['task_type']}\n"
        synthesis_prompt += f"Response: {result['response']}\n\n"
    synthesis_prompt += "Provide a concise, well-structured summary that integrates all the information coherently."

    synthesis_task = {
        "model": synthesis_model,
        "messages": [{"role": "user", "content": synthesis_prompt}],
    }

    synthesis_result = await run_llm_tasks([synthesis_task])
    return synthesis_result[0]['response'] if synthesis_result[0]['status'] == 'success' else "Synthesis failed"

async def process_prompt(user_prompt, selector):
    analyzer = OpenRouterPromptAnalyzer()
    sub_prompts = analyzer.analyze_prompt(user_prompt)

    if sub_prompts:
        tasks = [
            {
                "model": selector.select_llm(sub_prompt["task_type"])[0],
                "messages": [{"role": "user", "content": sub_prompt["text"]}],
                "task_type": sub_prompt["task_type"]
            }
            for sub_prompt in sub_prompts
        ]

        results = await run_llm_tasks(tasks, parallel=True)

        # Use an LLM for synthesis
        synthesis_model = selector.select_llm("synthesize")[0]
        synthesized_result = await synthesize_responses(results, synthesis_model)

        return results, synthesized_result
    else:
        return None, None

def render_main_interface():
    st.title("Orchestrator-LLM")

    # Initialize components
    selector = LLMSelector("model_config.json")

    # Input section
    st.header("Input your prompt")
    user_prompt = st.text_area("Enter your prompt here:", height=150)

    # Submit button
    if st.button("Submit"):
        if user_prompt:
            with st.spinner("Processing your request..."):
                try:
                    # Run the asynchronous processing
                    results, synthesized_result = asyncio.run(process_prompt(user_prompt, selector))

                    if results:
                        # Display individual LLM results
                        st.subheader("Individual LLM Results")
                        for result in results:
                            with st.expander(f"Task: {result['task']['messages'][0]['content'][:50]}..."):
                                st.write(f"Model: {result['task']['model']}")
                                st.write(f"Task Type: {result['task']['task_type']}")
                                st.write(f"Status: {result['status']}")
                                if result["status"] == "success":
                                    st.write(f"Response: {result['response']}")
                                else:
                                    st.error(f"Error: {result['error']}")

                        # Display synthesized result
                        st.subheader("Synthesized Result")
                        st.write(synthesized_result)

                    else:
                        st.error("Failed to analyze the prompt. Please try again.")

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

        else:
            st.warning("Please enter a prompt before submitting.")

    # Display system information
    st.sidebar.title("System Info")
    st.sidebar.info("Connected LLMs: 3")
    st.sidebar.info("System Status: Online")

    # Add a footer
    st.markdown("---")
    st.markdown("Orchestrator-LLM v0.1 - Powered by Streamlit")
