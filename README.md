# Introduction to Gen-AI in Python

This is a tutorial for those looking to get started programming GenAI-based applications in Python.

Lesson | Links
---    |---
Introduction | 📖 [Exercise](/src/chatbot/lessons/exercises/e00_intro/README.md)
Prompting | 📖 [Exercise](/src/chatbot/lessons/exercises/e01_prompting/README.md) ✅ [Solution](/src/chatbot/lessons/solutions/s01_prompting/README.md)
System instructions | 📖 [Exercise](/src/chatbot/lessons/exercises/e02_system_prompt/README.md) ✅ [Solution](/src/chatbot/lessons/solutions/s02_system_prompt/README.md)
Tracking conversation history | 📖 [Exercise](/src/chatbot/lessons/exercises/e03_conversation_history/README.md) ✅ [Solution](/src/chatbot/lessons/solutions/s03_conversation_history/README.md)
Structured outputs | 📖 [Exercise](/src/chatbot/lessons/exercises/e04_structured_outputs/README.md) ✅ [Solution](/src/chatbot/lessons/solutions/s04_structured_outputs/README.md)
Tool calling | 📖 [Exercise](/src/chatbot/lessons/exercises/e05_tool_calling/README.md) ✅ [Solution](/src/chatbot/lessons/solutions/s05_tool_calling/README.md)
Model Context Protocol (MCP) | 📖 [Exercise](/src/chatbot/lessons/exercises/e06_mcp/README.md) ✅ [Solution](/src/chatbot/lessons/solutions/s06_mcp/README.md)
Retrieval Augmented Generation (RAG) | 📖 [Exercise](/src/chatbot/lessons/exercises/e07_rag/README.md) ✅ [Solution](/src/chatbot/lessons/solutions/s07_rag/README.md)
Custom agent | 📖 [Exercise](/src/chatbot/lessons/exercises/e08_custom_agent/README.md) ✅ [Solution](/src/chatbot/lessons/solutions/s08_custom_agent/README.md)
Observability | 📖 [Exercise](/src/chatbot/lessons/exercises/e09_observability/README.md)

All of the above include automated test suites to verify and benchmark the implementation. For details, read the [Testing Guide](/src/chatbot/testing/README.md).

A basic [`streamlit`](https://docs.streamlit.io/get-started) chat UI is provided, so that the lessons can solely focus on the chatbot logic.

![Chat UI](/images/ui.png)

## Getting started

1. Clone this repo.

1. Install a recent version of Python 3 - options include:
    * using winget
    >
    > ```powershell
    > winget install --id Python.Python.3.13 --version 3.13.3 --scope user
    > ```

    * or [downloading](https://www.python.org/downloads/release/python-3133/) and installing somewhere accessible e.g. `%APPDATA%`.

1. Install uv, which will manage the project's Python package dependencies - options include:
    * using winget
    >
    > ```powershell
    > winget install --id astral-sh.uv --scope user
    > ```

    * or executing the [installation steps](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)

1. Install Ollama server, which will be used to launch local language models - options include:

    * using winget
    >
    > ```powershell
    > winget install --id Ollama.Ollama --scope user
    > ```

    * or [downloading](https://github.com/ollama/ollama/releases) and installing somewhere accessible e.g. `%APPDATA%`.

1. Use uv to create a Python virtual environment at the git clone location

    ```powershell
    uv venv --python 3.13.3
    ```

    and install the dependencies

    ```powershell
    uv sync
    ```

1. Start the app by running the command below in the clone location

    ```powershell
    uv run genai-chat
    ```

    If you make code changes to the chatbot logic while the app is running, you need to kill and restart it. Do this by issuing Ctrl-C in the terminal - simply closing the webpage is not enough, since the streamlit server continues to run!

1. Alternatively, each exercise can be run in console mode

    ```powershell
    uv run exercise-5
    ```

    or a corresponding solution

    ```powershell
    uv run solution-5
    ```
