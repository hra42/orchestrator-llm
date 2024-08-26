import streamlit as st

from internal.llmselector.v1 import LLMSelector
from internal.promptanalyzer.openrouter import OpenRouterPromptAnalyzer


def render_main_interface():
    st.title("Orchestrator-LLM")

    # Initialize LLMSelector
    selector = LLMSelector("model_config.json")

    # Input section
    st.header("Input your prompt")
    user_prompt = st.text_area("Enter your prompt here:", height=150)

    # Submit button
    if st.button("Submit"):
        if user_prompt:
            with st.spinner("Processing your request..."):
                # Analyze the prompt
                analyzer = OpenRouterPromptAnalyzer()
                sub_prompts = analyzer.analyze_prompt(user_prompt)

                if sub_prompts:
                    task_distribution = analyzer.get_task_distribution(sub_prompts)

                    # Display results
                    st.success("Request processed successfully!")
                    st.subheader("Prompt Analysis")
                    st.json(sub_prompts)

                    st.subheader("Task Distribution")
                    st.bar_chart(task_distribution)

                    # Use LLMSelector to distribute tasks
                    tasks = [
                        {
                            "task_type": sub_prompt["task_type"],
                            "prompt": sub_prompt["text"],
                        }
                        for sub_prompt in sub_prompts
                    ]
                    distribution = selector.distribute_tasks(tasks)

                    # Display LLM Selection Results
                    st.subheader("LLM Selection Results")
                    for model, model_tasks in distribution.items():
                        st.write(f"**{model}**")
                        for task in model_tasks:
                            st.write(f"- Task Type: {task['task_type']}")
                            st.write(f"  Prompt: {task['prompt']}")
                        st.write("")

                    # Here we would call the function to process the prompt with selected LLMs
                    # For now, we'll just display a placeholder result
                    st.subheader("LLM Results")
                    st.json(
                        {
                            "LLM1": "Sample response from LLM1",
                            "LLM2": "Sample response from LLM2",
                            "Synthesized": "Final synthesized response",
                        }
                    )
                else:
                    st.error(
                        "Failed to analyze the prompt. Please check the error messages above and try again."
                    )
        else:
            st.warning("Please enter a prompt before submitting.")

    # Display system information
    st.sidebar.title("System Info")
    st.sidebar.info("Connected LLMs: 3")
    st.sidebar.info("System Status: Online")

    # Add a footer
    st.markdown("---")
    st.markdown("Orchestrator-LLM v0.1 - Powered by Streamlit")
