# Multi Agent

다중 에이전트 시스템 예제입니다.

## 설명

이 예제는 LangGraph를 사용하여 여러 전문 에이전트가 협력하는 시스템을 구현합니다. Supervisor 패턴을 통해 작업을 적절한 에이전트에게 라우팅하고 결과를 조합합니다.

## 주요 구성 요소

- **Supervisor Pattern**: 작업 분배를 담당하는 슈퍼바이저
- **Specialized Agents**: 각각 특화된 기능을 가진 에이전트들
- **Agent Coordination**: 에이전트 간 협력 및 조정

## 사전 요구 사항

1. Ollama 설치 및 실행
2. OpenAI API 키 (다중 에이전트 기능을 위해 권장)
3. Tavily API 키 (웹 검색 기능용, 선택사항)
4. 환경 변수 설정:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export TAVILY_API_KEY="your-tavily-api-key"  # 선택사항
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch08/04_multi_agent
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. 다양한 유형의 작업을 요청하여 각 에이전트의 전문성을 확인하세요.

## 그래프 구조 확인

프로젝트 디렉토리에 `graph.png` 파일이 생성되어 다중 에이전트 시스템의 구조를 시각적으로 확인할 수 있습니다.