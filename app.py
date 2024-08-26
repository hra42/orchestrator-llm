import os

import streamlit as st
from dotenv import load_dotenv

from internal.intro import get_intro
from internal.ui.ui import render_main_interface

# Load environment variables from .env file
load_dotenv()

# Verify that the API key is set
if not os.environ.get("OPENROUTER_API_KEY"):
    st.error("OPENROUTER_API_KEY is not set in the environment variables.")
    st.stop()

st.set_page_config(page_title="Orchestrator-LLM", page_icon="🤖", layout="wide")

# MARK: - Pages List
page_names_to_funcs = {
    "-": get_intro,
    "Orchestrator-LLM": render_main_interface,
}

# MARK: - Sidebar
orchestrator_llm = st.sidebar.selectbox(
    "Choose a function", list(page_names_to_funcs.keys())
)
orchestrator_llm = (
    orchestrator_llm or "-"
)  # Assign a default value if orchestrator_llm is None
page_names_to_funcs[orchestrator_llm]()
