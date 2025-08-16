# Basic Chatbot Graph

LangGraph를 사용한 기본 챗봇 그래프 예제입니다.

## 설명

이 예제는 LangGraph를 사용하여 상태 기반 대화 시스템을 구현하는 방법을 보여줍니다. 그래프 구조를 통해 대화 흐름을 체계적으로 관리할 수 있습니다.

## 주요 구성 요소

- **StateGraph**: 상태 기반 그래프 구조
- **Conversation Flow**: 체계적인 대화 흐름 관리
- **Memory Management**: 대화 상태 및 메모리 관리

## 사전 요구 사항

1. Ollama 설치 및 실행
2. Qwen3 모델 다운로드:
   ```bash
   ollama pull qwen3:8b
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch08/01_basic_chatbot_graph
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. 그래프 기반 챗봇과 대화를 나누어 보세요.