# LangChain Hub

LangChain Hub를 사용한 프롬프트 관리 예제입니다.

## 설명

이 예제는 LangChain Hub를 활용하여 공유된 프롬프트 템플릿을 사용하고 관리하는 방법을 보여줍니다. 커뮤니티에서 검증된 프롬프트를 활용하여 더 나은 결과를 얻을 수 있습니다.

## 주요 구성 요소

- **LangChain Hub**: 공유 프롬프트 저장소
- **Prompt Templates**: 검증된 프롬프트 템플릿 활용
- **Community Resources**: 커뮤니티 기여 프롬프트 사용

## 사전 요구 사항

1. Ollama 설치 및 실행
2. LangChain API 키 (Hub 사용을 위해)
3. 환경 변수 설정:
   ```bash
   export LANGCHAIN_API_KEY="your-langchain-api-key"
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch06/02_langchain_hub
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. Hub에서 가져온 프롬프트가 적용된 응답을 확인하세요.