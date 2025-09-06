# OpenAI Chat

OpenAI API를 사용한 LangChain 채팅 예제입니다.

## 설명

이 예제는 LangChain과 OpenAI API를 사용하여 채팅 애플리케이션을 구현합니다. Ollama 대신 OpenAI의 GPT 모델을 사용하는 방법을 보여줍니다.

## 주요 구성 요소

- **ChatOpenAI**: OpenAI 모델과 연결하는 LangChain 인터페이스
- **API 키 관리**: 환경 변수를 통한 안전한 API 키 관리
- **대화 인터페이스**: 사용자와 AI 간의 대화 구조

## 사전 요구 사항

1. OpenAI API 키 ([OpenAI 웹사이트](https://platform.openai.com/)에서 발급)
2. 환경 변수 설정:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   또는 `.env` 파일에 추가:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch03/02_openai_chat
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