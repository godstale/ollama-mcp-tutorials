# Output Parser

구조화된 출력을 생성하는 예제입니다.

## 설명

이 예제는 LangChain의 Output Parser를 사용하여 AI 모델의 응답을 구조화된 형태로 파싱하는 방법을 보여줍니다. JSON, Pydantic 모델 등을 활용하여 일관된 형식의 출력을 얻을 수 있습니다.

## 주요 구성 요소

- **Output Parser**: AI 응답을 구조화된 형태로 변환
- **Pydantic 모델**: 타입 안전성을 보장하는 데이터 구조
- **구조화된 응답**: 일관된 형식의 출력 보장

## 사전 요구 사항

1. Ollama 설치 및 실행
2. Qwen3:8b 모델 다운로드
   ```bash
   ollama pull qwen3:8b
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch03/04_output_parser
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. 질문을 입력하고 구조화된 형식의 응답을 확인하세요.