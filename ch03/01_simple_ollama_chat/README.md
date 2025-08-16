# Simple Ollama Chat

기본적인 Ollama를 사용한 LangChain 채팅 예제입니다.

## 설명

이 예제는 LangChain과 Ollama를 사용하여 가장 간단한 형태의 대화형 챗봇을 구현합니다. 사용자의 입력을 받아 Ollama 모델에 전달하고 응답을 출력하는 기본적인 구조를 보여줍니다.

## 주요 구성 요소

- **ChatOllama**: Ollama 모델과 연결하는 LangChain 인터페이스
- **HumanMessage**: 사용자 메시지를 포장하는 LangChain 메시지 클래스
- **대화 루프**: 사용자 입력을 받고 응답을 출력하는 기본 구조

## 사전 요구 사항

1. Ollama 설치 및 실행
2. Qwen3:8b 모델 다운로드
   ```bash
   ollama pull qwen3:8b
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch03/01_simple_ollama_chat
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. 질문을 입력하고 응답을 확인하세요. 종료하려면 'exit'를 입력하세요.