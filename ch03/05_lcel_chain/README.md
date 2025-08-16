# LCEL Chain

LangChain Expression Language(LCEL)를 사용한 체인 구성 예제입니다.

## 설명

이 예제는 LangChain Expression Language(LCEL)를 사용하여 여러 구성 요소를 연결하는 체인을 만드는 방법을 보여줍니다. 프롬프트, 모델, 파서를 파이프라인으로 연결하여 효율적인 처리 흐름을 구현합니다.

## 주요 구성 요소

- **LCEL**: LangChain Expression Language를 통한 체인 구성
- **파이프라인**: 프롬프트 → 모델 → 파서의 연결된 처리 흐름
- **모듈화**: 재사용 가능한 구성 요소들의 조합

## 사전 요구 사항

1. Ollama 설치 및 실행
2. Qwen3:8b 모델 다운로드
   ```bash
   ollama pull qwen3:8b
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch03/05_lcel_chain
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. 질문을 입력하고 체인을 통해 처리된 응답을 확인하세요.