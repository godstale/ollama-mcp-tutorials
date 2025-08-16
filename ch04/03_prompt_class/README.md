# Prompt Class

프롬프트 클래스를 사용한 고급 프롬프트 관리 예제입니다.

## 설명

이 예제는 LangChain의 Prompt 클래스를 사용하여 더 복잡하고 체계적인 프롬프트 관리 방법을 보여줍니다. 다양한 타입의 프롬프트와 템플릿을 객체지향 방식으로 관리할 수 있습니다.

## 주요 구성 요소

- **Prompt Classes**: 객체지향 프롬프트 관리
- **Template Management**: 체계적인 템플릿 구조
- **Advanced Formatting**: 고급 형식 지정 기능

## 사전 요구 사항

1. Ollama 설치 및 실행
2. Qwen3:8b 모델 다운로드
   ```bash
   ollama pull qwen3:8b
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch04/03_prompt_class
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. 질문을 입력하고 고급 프롬프트 클래스가 적용된 응답을 확인하세요.