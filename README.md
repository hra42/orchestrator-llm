# Orchestrator-LLM

## Overview

Orchestrator-LLM is a proof-of-concept tool designed to orchestrate the execution of multiple Large Language Models (LLMs) in parallel. Our goal is to provide a simple, user-friendly interface that allows users to leverage the power of various AI models without needing to understand the intricacies of each model's strengths and weaknesses.

## Features

- Parallel execution of multiple LLMs
- Intelligent task distribution based on model strengths
- User-friendly interface for prompt input and result visualization
- Seamless integration of various LLM APIs

## Getting Started

These instructions will help you set up and run Orchestrator-LLM on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/Orchestrator-LLM.git
   cd Orchestrator-LLM
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up environment variables (if necessary):
   ```sh
   cp .env.example .env
   # Edit .env file with your API keys and other configurations
   ```

### Running the App

To run the Streamlit app locally:

```sh
streamlit run app.py
```

The app should now be running on `http://localhost:8501`.

### Docker Support

To run the app using Docker:

```sh
docker run -p 8501:8501 -d --name orchestrator-llm ghcr.io/HRA42/orchestrator-llm:latest
```

Note: Docker image is coming soon. The repository will be updated with Dockerfile and build instructions.

## Usage

1. Open the app in your web browser
2. Enter your prompt in the text input field
3. Click "Submit" to process your request
4. View the orchestrated results from multiple LLMs

## Built With

- [Streamlit](https://streamlit.io/) - The web framework for creating data apps
- [Python](https://www.python.org/) - The core programming language
- Various LLM APIs (details to be added)
