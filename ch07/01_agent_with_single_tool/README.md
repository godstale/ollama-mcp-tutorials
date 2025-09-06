# Agent with Single Tool

단일 도구를 사용하는 에이전트 예제입니다.

## 설명

이 예제는 LangChain 에이전트가 하나의 도구를 사용하여 작업을 수행하는 방법을 보여줍니다. 에이전트가 언제 도구를 사용해야 하는지 판단하고 실행하는 기본적인 ReAct 패턴을 구현합니다.

## 주요 구성 요소

- **Single Tool Agent**: 하나의 도구를 가진 에이전트
- **ReAct Pattern**: Reasoning과 Acting을 결합한 패턴
- **Tool Integration**: 도구 통합 및 활용

## 사전 요구 사항

1. Ollama 설치 및 실행
2. 도구 사용이 가능한 모델:
   ```bash
   ollama pull qwen3:8b
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch07/01_agent_with_single_tool
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. 도구가 필요한 작업을 요청하고 에이전트의 동작을 확인하세요.