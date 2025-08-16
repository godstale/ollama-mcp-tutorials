# Agent with Multi Tools

여러 도구를 사용하는 에이전트 예제입니다.

## 설명

이 예제는 LangChain 에이전트가 여러 도구 중에서 적절한 도구를 선택하여 작업을 수행하는 방법을 보여줍니다. 복잡한 작업을 수행하기 위해 여러 도구를 조합하여 사용할 수 있습니다.

## 주요 구성 요소

- **Multi-Tool Agent**: 여러 도구를 가진 에이전트
- **Tool Selection**: 상황에 맞는 도구 선택
- **Complex Workflows**: 복합적인 작업 수행

## 사전 요구 사항

1. Ollama 설치 및 실행
2. 도구 사용이 가능한 모델:
   ```bash
   ollama pull qwen3:8b
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch07/02_agent_with_multi_tools
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. 다양한 유형의 작업을 요청하고 에이전트가 적절한 도구를 선택하는지 확인하세요.