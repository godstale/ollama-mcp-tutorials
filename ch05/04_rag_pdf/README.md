# RAG PDF

PDF 문서를 활용한 RAG(Retrieval-Augmented Generation) 예제입니다.

## 설명

이 예제는 PDF 문서를 로드하고 처리하여 벡터 스토어에 저장한 후, 사용자 질문에 대해 PDF 내용을 검색하여 답변을 생성하는 RAG 시스템을 구현합니다. 문서 기반 질의응답 시스템의 기본 구조를 보여줍니다.

## 주요 구성 요소

- **PDF Processing**: PDF 문서 로드 및 텍스트 추출
- **Document Chunking**: 문서를 적절한 크기로 분할
- **RAG Implementation**: PDF 내용 기반 질의응답 시스템

## 사전 요구 사항

1. Ollama 설치 및 실행
2. 필요한 모델 다운로드:
   ```bash
   ollama pull qwen3:8b
   ollama pull nomic-embed-text
   ```
3. PDF 파일 준비 (예제에는 `news_weather.pdf` 포함)

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch05/04_rag_pdf
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. PDF 내용에 관한 질문을 입력하고 답변을 확인하세요.