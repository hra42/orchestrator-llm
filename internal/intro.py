import streamlit as st


# MARK: - Home
def get_intro():
    st.title("Welcome to Orchestrator-LLM: A Proof of Concept")

    st.markdown("""
    ## What is Orchestrator-LLM?

    Orchestrator-LLM is an innovative proof-of-concept tool designed to seamlessly manage multiple Large Language Models (LLMs) in parallel. Our goal is to provide a user-friendly interface that allows you to harness the power of various AI models without needing to understand the intricacies of each one's strengths and weaknesses.

    ## How does it work?

    At its core, Orchestrator-LLM acts as an intelligent intermediary between you and a diverse array of LLMs. Here's how the magic happens:

    1. When you input a prompt, Orchestrator-LLM analyzes and breaks it down into smaller, targeted components.
    2. These components are then distributed to different LLMs, each specialized in handling specific types of queries.
    3. The LLMs process their assigned tasks and generate responses.
    4. Orchestrator-LLM collects these individual outputs, synthesizes them, and presents you with a comprehensive result.

    This approach allows us to leverage the unique strengths of multiple AI models, providing you with more nuanced and accurate responses.

    ### Visual Representation

    To better illustrate this process, here's a simplified diagram of Orchestrator-LLM in action:
    """)
    st.image("./media/idea.png", use_column_width=True)
