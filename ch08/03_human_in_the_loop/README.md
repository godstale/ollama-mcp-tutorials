# Human in the Loop

사람이 개입하는 루프가 있는 LangGraph 예제입니다.

## 설명

이 예제는 LangGraph에 인간의 개입(Human-in-the-loop)을 포함하는 시스템을 구현합니다. 중요한 결정이나 검토가 필요한 단계에서 사용자의 확인을 받을 수 있습니다.

## 주요 구성 요소

- **Human Intervention**: 중요 단계에서 사용자 개입
- **Approval Workflow**: 승인 기반 워크플로우
- **Interactive Graph**: 상호작용 가능한 그래프 시스템

## 사전 요구 사항

1. Ollama 설치 및 실행
2. OpenAI API 키 (권장)
3. 환경 변수 설정:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch08/03_human_in_the_loop
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. 시스템이 승인을 요청할 때 적절히 응답하세요.

## 그래프 구조 확인

프로젝트 디렉토리에 `graph.png` 파일이 생성되어 그래프 구조를 시각적으로 확인할 수 있습니다.