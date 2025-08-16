# Vector Store

벡터 스토어를 사용한 문서 저장 및 검색 예제입니다.

## 설명

이 예제는 LangChain의 Vector Store를 사용하여 문서를 벡터 형태로 저장하고 검색하는 방법을 보여줍니다. 문서의 의미적 유사성을 기반으로 관련 문서를 효율적으로 찾을 수 있습니다.

## 주요 구성 요소

- **Vector Store**: 벡터화된 문서 저장소
- **Document Indexing**: 문서의 벡터화 및 인덱싱
- **Semantic Search**: 의미 기반 문서 검색

## 사전 요구 사항

1. Ollama 설치 및 실행
2. 임베딩 모델 다운로드
   ```bash
   ollama pull nomic-embed-text
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch05/02_vector_store
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. 검색 쿼리를 입력하고 관련 문서를 확인하세요.