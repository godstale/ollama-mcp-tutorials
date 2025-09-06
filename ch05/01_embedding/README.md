# Embedding

텍스트 임베딩 생성 및 활용 예제입니다.

## 설명

이 예제는 LangChain을 사용하여 텍스트를 벡터 임베딩으로 변환하는 방법을 보여줍니다. 임베딩은 텍스트의 의미를 수치적으로 표현하여 유사도 계산, 검색, 분류 등에 활용할 수 있습니다.

## 주요 구성 요소

- **Text Embedding**: 텍스트를 벡터로 변환
- **Similarity Search**: 벡터 유사도를 통한 검색
- **Semantic Understanding**: 의미적 유사성 파악

## 사전 요구 사항

1. Ollama 설치 및 실행
2. 임베딩 모델 다운로드 (예: nomic-embed-text)
   ```bash
   ollama pull nomic-embed-text
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch05/01_embedding
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. 텍스트를 입력하고 임베딩 벡터와 유사도를 확인하세요.