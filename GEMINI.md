# Project: AI Agent Programming Guide

## Project Overview

This repository contains a series of Python-based tutorials on building AI agents. It serves as a programming guide for developers who want to learn and implement AI agent systems using modern technologies. The tutorials are organized into chapters, each focusing on a specific aspect of agent development, from basic concepts to advanced multi-agent systems.

The core technologies used in this project are:

*   **LangChain & LangGraph:** For building and composing AI applications and agents.
*   **Ollama:** For running local large language models.
*   **MCP (Model Context Protocol):** A protocol for advanced agent communication.
*   **Python:** The primary programming language.
*   **UV:** The package manager used for dependency management.

## Building and Running

The project is divided into chapters, and each chapter contains one or more independent Python projects. To run a specific project:

1.  **Navigate to the project directory:**
    ```bash
    cd ch11 # or another chapter directory
    ```

2.  **Install dependencies using UV:**
    ```bash
    uv sync
    ```

3.  **Run the main script:**
    ```bash
    uv run python main.py
    ```
    Some projects may require command-line arguments. For example:
    ```bash
    uv run python main.py --audio-path path/to/audio.mp3 --save
    ```

## Development Conventions

The project follows standard Python development conventions.

*   **Package Management:** The `uv` package manager is used for dependency management. Dependencies for each project are listed in `pyproject.toml`, and the exact versions are locked in `uv.lock`.
*   **Code Style:** The codebase is formatted using `black` and `isort`.
*   **Type Checking:** `mypy` is used for static type checking.
*   **Testing:** `pytest` is used for running tests.

The following commands can be used to maintain code quality:

*   **Formatting:**
    ```bash
    uv run black .
    uv run isort .
    ```
*   **Type Checking:**
    ```bash
    uv run mypy .
    ```
*   **Testing:**
    ```bash
    uv run pytest
    ```

## Environment Configuration

Some projects require API keys to be set as environment variables. These include:

*   `OPENAI_API_KEY`: For projects using OpenAI models.
*   `LANGCHAIN_API_KEY`: For tracing with LangSmith (Chapter 6).
*   `TAVILY_API_KEY`: For web search tools (Chapter 8).

These should be set in your shell environment before running the projects.
