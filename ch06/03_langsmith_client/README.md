# LangSmith Client

LangSmith Client를 사용한 데이터셋 관리 및 평가 예제입니다.

## 설명

이 예제는 LangSmith Client를 직접 사용하여 데이터셋을 생성하고 관리하며, 모델 성능을 평가하는 방법을 보여줍니다. 체계적인 실험 관리와 성능 측정이 가능합니다.

## 주요 구성 요소

- **LangSmith Client**: 직접적인 LangSmith API 사용
- **Dataset Management**: 데이터셋 생성 및 관리
- **Model Evaluation**: 모델 성능 평가 및 비교

## 사전 요구 사항

1. Ollama 설치 및 실행
2. LangSmith 계정 및 API 키
3. 환경 변수 설정:
   ```bash
   export LANGCHAIN_API_KEY="your-langsmith-api-key"
   export LANGCHAIN_TRACING_V2=true
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch06/03_langsmith_client
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. 데이터셋 생성 및 평가 과정을 확인하세요.