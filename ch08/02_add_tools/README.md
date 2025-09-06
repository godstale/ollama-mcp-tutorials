# Add Tools

LangGraph에 도구를 추가한 예제입니다.

## 설명

이 예제는 LangGraph 기반 시스템에 도구를 통합하여 더 강력한 기능을 제공하는 방법을 보여줍니다. 그래프 구조 내에서 도구를 활용하여 복잡한 작업을 수행할 수 있습니다.

## 주요 구성 요소

- **Tool Integration**: 그래프에 도구 통합
- **Enhanced Capabilities**: 도구를 통한 기능 확장
- **Workflow Management**: 도구를 포함한 워크플로우 관리

## 사전 요구 사항

1. Ollama 설치 및 실행
2. OpenAI API 키 (도구 사용을 위해 권장)
3. 환경 변수 설정:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch08/02_add_tools
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. 도구가 통합된 그래프 시스템을 사용해 보세요.