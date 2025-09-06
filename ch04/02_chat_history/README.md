# Chat History

대화 기록을 유지하는 채팅 예제입니다.

## 설명

이 예제는 LangChain을 사용하여 대화 기록을 관리하고 유지하는 방법을 보여줍니다. 이전 대화 내용을 기억하여 문맥을 이해하고 연속적인 대화를 가능하게 합니다.

## 주요 구성 요소

- **Chat History**: 대화 기록 저장 및 관리
- **Memory**: 이전 대화 내용을 기억하는 메모리 시스템
- **Context Awareness**: 문맥을 고려한 응답 생성

## 사전 요구 사항

1. Ollama 설치 및 실행
2. Qwen3:8b 모델 다운로드
   ```bash
   ollama pull qwen3:8b
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch04/02_chat_history
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. 연속적인 대화를 나누며 이전 대화 내용이 기억되는지 확인하세요.