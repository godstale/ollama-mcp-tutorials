# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains example code for an AI agent programming guide using LangChain and LangGraph with MCP (Model Context Protocol). The project is organized into progressive chapters (ch03-ch11) that teach AI agent development from basic Ollama chat to advanced MCP-enabled multi-agent systems.

### Educational Progression
- **ch03**: Basic LangChain concepts with Ollama
- **ch04**: Prompt engineering and chat history
- **ch05**: RAG (Retrieval-Augmented Generation) implementations
- **ch06**: Observability and tracing with LangSmith
- **ch07**: Tool-enabled agents
- **ch08**: Multi-agent systems with LangGraph
- **ch09**: MCP protocol integration
- **ch10**: Advanced MCP use cases
- **ch11**: Real-world application (meeting transcription)

## Development Commands

### Running Individual Projects
Each chapter contains independent Python projects with their own dependencies:

```bash
# Navigate to any chapter/project directory
cd ch11  # or ch09/01_mcp_agent, etc.

# Install dependencies
uv sync

# Run the main script
uv run python main.py

# For projects with CLI arguments (like ch11)
uv run python main.py --audio-path path/to/audio.mp3 --save
```

### Development Tools (where available)
Some projects include development dependencies:

```bash
# Code formatting
uv run black .
uv run isort .

# Type checking
uv run mypy .

# Testing
uv run pytest
```

## Architecture Overview

### Project Structure Pattern
Most chapters follow this structure:
- `main.py` - Entry point and CLI interface
- `pyproject.toml` - Dependencies and project configuration
- `src/` - Core implementation modules (in more complex projects)

### Key Architectural Patterns

#### 1. LangChain Integration (ch03-ch07)
- Uses `ChatOllama` for local LLM integration
- Implements chains with LCEL (LangChain Expression Language)
- Progressive complexity: basic chat → tools → agents

#### 2. LangGraph Multi-Agent Systems (ch08)
- Supervisor pattern for agent coordination
- State management with `AgentState` TypedDict
- Conditional routing between specialized agents
- Memory persistence with checkpointers

#### 3. MCP (Model Context Protocol) Integration (ch09-ch10)
- `mcp_manager.py` - MCP client lifecycle management
- `mcp_config.json` - Server configuration
- `langchain_mcp_adapters` for tool integration
- Async patterns for MCP communication

#### 4. Audio Processing Pipeline (ch11)
- Modular pipeline: `AudioTranscriber` → `MeetingSummarizer`
- Uses `faster-whisper` for speech recognition
- Structured output generation with LLM prompts

### Common Dependencies
- **LangChain ecosystem**: `langchain-core`, `langchain-ollama`, `langchain-community`
- **LangGraph**: State graphs, checkpointing, prebuilt agents
- **MCP**: `mcp`, `langchain-mcp-adapters` for protocol integration
- **Local LLM**: Ollama for running models locally

### Development Patterns

#### Error Handling
- Async context managers for MCP clients (`__aenter__`/`__aexit__`)
- Try-catch blocks with cleanup in finally blocks
- Graceful degradation when services unavailable

#### Configuration Management
- Environment variables via `python-dotenv`
- JSON configuration files for MCP servers
- CLI argument parsing with `argparse`

#### State Management
- TypedDict for structured state in LangGraph
- Message annotation with `add_messages`
- Thread-based conversation memory

## Prerequisites

### Required Services
- **Ollama**: Install and run locally for LLM inference
- **Models**: Pull required models (e.g., `ollama pull qwen3:8b`)

### Environment Setup
- Python 3.10+ (some projects require 3.12+)
- UV package manager for dependency management
- Optional: OpenAI API key for projects using GPT models
- Optional: LangSmith API key for tracing (ch06)
- Optional: Tavily API key for web search tools (ch08)

## Chapter-Specific Notes

### ch03-ch05: Foundation Concepts
- **ch03**: Basic Ollama integration, streaming, and output parsing
- **ch04**: Prompt templates and conversation memory
- **ch05**: Vector stores, embeddings, and RAG patterns

### ch06: Observability
- LangSmith integration for tracing and monitoring
- Dataset management and evaluation

### ch07: Tool-Enabled Agents
- Single and multi-tool agent implementations
- ReAct pattern with LangChain agents

### ch08: Multi-Agent Systems
- Complex state routing logic
- Supervisor pattern for agent coordination
- Graph visualization capabilities

### ch09-ch10: MCP Integration
- Require proper MCP server configuration in `mcp_config.json`
- Use async/await patterns throughout
- Handle MCP client lifecycle carefully
- **ch09**: Basic MCP agent with weather tools
- **ch10**: Advanced MCP integrations (Notion, news aggregation)

### ch11: Real-world Application  
- **ch11**: Meeting transcription system using LangGraph workflows
- Features audio processing pipeline with structured state management
- Implements modular components: transcriber, summarizer, file handler
- Uses Faster Whisper for speech-to-text and Ollama for summarization

## Development Commands by Chapter

### Chapter 11 (Current - Meeting Notes Pipeline)
```bash
# Navigate to ch11 directory
cd ch11

# Install dependencies 
uv sync

# Run with default sample audio
uv run python main.py

# Process custom audio file with save
uv run python main.py --audio-path path/to/audio.mp3 --save

# Specify output location
uv run python main.py --audio-path input.mp3 --output meeting_notes.md --save

# Use different Whisper model size
uv run python main.py --model-size large --llm-model llama3:8b

# Development tools (when available)
uv run black .
uv run isort .
uv run mypy .
```

### Code Style Guidelines
Ch11 follows specific Korean coding conventions defined in `coding_rules.md`:
- Comments and user interface in Korean
- Snake_case for variables/functions, PascalCase for classes
- Structured error handling with Korean error messages
- F-string formatting preferred for all string interpolation
- Sequential step numbering in comments (`# 1.`, `# 2.`, etc.)

## Learning Path Recommendations

1. **Start with ch03** for basic LangChain concepts
2. **Progress through ch04-ch05** for foundational patterns  
3. **Use ch06** to understand observability early in development
4. **Explore ch07-ch08** for agent architectures
5. **Advance to ch09-ch10** for cutting-edge MCP integration
6. **Complete with ch11** for real-world application implementation