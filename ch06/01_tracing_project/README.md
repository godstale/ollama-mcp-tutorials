# Tracing Project

LangSmith를 사용한 추적 및 모니터링 예제입니다.

## 설명

이 예제는 LangSmith를 사용하여 LangChain 애플리케이션의 실행 과정을 추적하고 모니터링하는 방법을 보여줍니다. 디버깅, 성능 분석, 품질 개선에 도움이 됩니다.

## 주요 구성 요소

- **LangSmith Tracing**: 애플리케이션 실행 추적
- **Performance Monitoring**: 성능 메트릭 모니터링
- **Debug Capabilities**: 디버깅 및 문제 해결 도구

## 사전 요구 사항

1. Ollama 설치 및 실행
2. LangSmith 계정 및 API 키 ([LangSmith](https://smith.langchain.com/)에서 발급)
3. 환경 변수 설정:
   ```bash
   export LANGCHAIN_TRACING_V2=true
   export LANGCHAIN_API_KEY="your-langsmith-api-key"
   export LANGCHAIN_PROJECT="your-project-name"
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch06/01_tracing_project
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. 질문을 입력하고 LangSmith 대시보드에서 추적 정보를 확인하세요.

## LangSmith 대시보드 확인

실행 후 LangSmith 웹 인터페이스에서 다음을 확인할 수 있습니다:
- 실행 추적(Trace) 정보
- 각 단계별 소요 시간
- 입력/출력 데이터
- 오류 및 성능 메트릭