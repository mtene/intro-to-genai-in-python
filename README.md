# Introduction to Gen-AI in Python

This is a tutorial for those looking to get started programming GenAI-based applications in Python.

Lesson | Links
---    |---
Introduction | 📖 [Exercise](/src/chatbot/lessons/step0_intro/README.md)
Prompting | 📖 [Exercise](/src/chatbot/lessons/step1_prompting/README.md) ✅ [Solution](/src/chatbot/lessons/step1_prompting_solution/README.md)
System instructions | 📖 [Exercise](/src/chatbot/lessons/step2_system_prompt/README.md) ✅ [Solution](/src/chatbot/lessons/step2_system_prompt_solution/README.md)
Tracking conversation history | 📖 [Exercise](/src/chatbot/lessons/step3_conversation_history/README.md) ✅ [Solution](/src/chatbot/lessons/step3_conversation_history_solution/README.md)
Structured outputs | 📖 [Exercise](/src/chatbot/lessons/step4_structured_outputs/README.md) ✅ [Solution](/src/chatbot/lessons/step4_structured_outputs_solution/README.md)
Tool calling | 📖 [Exercise](/src/chatbot/lessons/step5_tool_calling/README.md) ✅ [Solution](/src/chatbot/lessons/step5_tool_calling_solution/README.md)
Custom agent | 📖 [Exercise](/src/chatbot/lessons/step6_custom_agent/README.md) ✅ [Solution](/src/chatbot/lessons/step6_custom_agent_solution/README.md)

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

    * using pip
    >
    > ```powershell
    > pip install uv
    > ```

    * executing the [installation steps](https://docs.astral.sh/uv/getting-started/installation/#installation-methods) via powershell
    >
    > ```powershell
    > powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    > ```

1. Install Ollama server, which will be used to launch local language models - options include:

    * using winget
    >
    > ```powershell
    > winget install --id Ollama.Ollama --scope user
    > ```

    * or [downloading](https://github.com/ollama/ollama/releases/tag/v0.12.3) and installing somewhere accessible e.g. `%APPDATA%`.

1. Use uv to setup the dependencies by running the following command at the git clone location

    ```powershell
    uv sync
    ```

1. Start the app by running the command below in the clone location

    ```powershell
    uv run genai-chat
    ```

    If you make code changes to the chatbot logic while the app is running, you need to kill and restart it. Do this by issuing Ctrl-C in the terminal - simply closing the webpage is not enough, since the streamlit server continues to run!

1. Alternatively, each lesson can be run in console mode

    ```powershell
    uv run step-5
    ```

    or a corresponding solution

    ```powershell
    uv run step-5-solution
    ```
