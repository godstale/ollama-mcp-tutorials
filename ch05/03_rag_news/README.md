# RAG News

뉴스 데이터를 활용한 RAG(Retrieval-Augmented Generation) 예제입니다.

## 설명

이 예제는 뉴스 데이터를 벡터 스토어에 저장하고, 사용자 질문에 관련된 뉴스를 검색하여 답변을 생성하는 RAG 시스템을 구현합니다. 실시간 정보를 활용한 정확한 답변을 제공할 수 있습니다.

## 주요 구성 요소

- **RAG Pipeline**: 검색-증강 생성 파이프라인
- **News Data**: 뉴스 데이터 수집 및 처리
- **Context-Aware Responses**: 검색된 문맥을 활용한 답변 생성

## 사전 요구 사항

1. Ollama 설치 및 실행
2. 필요한 모델 다운로드:
   ```bash
   ollama pull qwen3:8b
   ollama pull nomic-embed-text
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch05/03_rag_news
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. 뉴스 관련 질문을 입력하고 검색된 정보를 바탕으로 한 답변을 확인하세요.