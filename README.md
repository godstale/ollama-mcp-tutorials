# AI Agent Programming Guide: LangChain & LangGraph with MCP

LangChain과 LangGraph를 활용한 AI 에이전트 프로그래밍 가이드입니다. 기본적인 Ollama 챗봇부터 고급 MCP(Model Context Protocol) 기반 멀티 에이전트 시스템까지 단계별로 학습할 수 있습니다.

## 📚 프로젝트 구성

### 학습 진도표
- **ch03**: LangChain 기본 개념과 Ollama 통합
- **ch04**: 프롬프트 엔지니어링과 대화 히스토리
- **ch05**: RAG(검색 증강 생성) 구현
- **ch06**: LangSmith를 활용한 관찰 가능성과 추적
- **ch07**: 도구 지원 에이전트
- **ch08**: LangGraph를 활용한 멀티 에이전트 시스템
- **ch09**: MCP 프로토콜 통합
- **ch10**: 고급 MCP 활용 사례
- **ch11**: 실제 애플리케이션 (회의록 자동 생성)

## 🚀 시작하기

### 필수 사전 설치

1. **Python 3.10+** (일부 프로젝트는 3.12+ 요구)
2. **UV 패키지 매니저**
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Ollama 설치 및 실행**
   ```bash
   # Ollama 설치 (https://ollama.com/download)
   # 모델 다운로드
   ollama pull qwen2.5:7b
   ollama pull llama3:8b
   ```

### 프로젝트 실행 방법

각 챕터는 독립적인 Python 프로젝트입니다:

```bash
# 원하는 챕터/프로젝트 디렉토리로 이동
cd ch11  # 또는 ch09/01_mcp_agent 등

# 의존성 설치
uv sync

# 메인 스크립트 실행
uv run python main.py

# CLI 인자가 있는 프로젝트의 경우 (ch11)
uv run python main.py --audio-path path/to/audio.mp3 --save
```

## 📋 챕터별 상세 내용

### ch03-ch05: 기초 개념
- **ch03**: Ollama 통합, 스트리밍, 출력 파싱
- **ch04**: 프롬프트 템플릿과 대화 메모리
- **ch05**: 벡터 스토어, 임베딩, RAG 패턴

### ch06: 관찰 가능성
- LangSmith 통합을 통한 추적 및 모니터링
- 데이터셋 관리와 평가

### ch07: 도구 지원 에이전트
- 단일 및 다중 도구 에이전트 구현
- LangChain 에이전트의 ReAct 패턴

### ch08: 멀티 에이전트 시스템
- 복잡한 상태 라우팅 로직
- 에이전트 조정을 위한 슈퍼바이저 패턴
- 그래프 시각화 기능

### ch09-ch10: MCP 통합
- `mcp_config.json`에서 적절한 MCP 서버 구성 필요
- 전체적으로 async/await 패턴 사용
- MCP 클라이언트 라이프사이클 신중한 처리
- **ch09**: 날씨 도구가 포함된 기본 MCP 에이전트
- **ch10**: 고급 MCP 통합 (Notion, 뉴스 수집)

### ch11: 실제 애플리케이션
- LangGraph 워크플로를 사용한 회의록 자동 생성 시스템
- 구조화된 상태 관리를 갖춘 오디오 처리 파이프라인
- 모듈형 구성 요소: 전사기, 요약기, 파일 핸들러
- 음성-텍스트 변환에는 Faster Whisper, 요약에는 Ollama 사용

## 🛠️ 개발 도구 (사용 가능한 경우)

```bash
# 코드 포맷팅
uv run black .
uv run isort .

# 타입 검사
uv run mypy .

# 테스트
uv run pytest
```

## 📝 환경 설정 (선택사항)

일부 프로젝트에서 필요한 환경 변수:

```bash
# OpenAI API 키 (GPT 모델 사용 프로젝트)
export OPENAI_API_KEY="your-api-key"

# LangSmith API 키 (ch06 추적)
export LANGCHAIN_API_KEY="your-langsmith-key"

# Tavily API 키 (ch08 웹 검색 도구)
export TAVILY_API_KEY="your-tavily-key"
```

## 🎯 추천 학습 경로

1. **ch03부터 시작** - 기본 LangChain 개념
2. **ch04-ch05 진행** - 기초 패턴들
3. **ch06 활용** - 개발 초기에 관찰 가능성 이해
4. **ch07-ch08 탐색** - 에이전트 아키텍처
5. **ch09-ch10 진행** - 최신 MCP 통합
6. **ch11로 완료** - 실제 애플리케이션 구현

## 🔗 Colab 노트북 링크

각 챕터는 Google Colab에서 직접 실행할 수 있는 노트북도 제공합니다:

### ch03
- [01_simple_ollama_chat](https://colab.research.google.com/drive/1uh-K7fksjHmqx6OOyYo6zzhBGw0x4oj8?usp=drive_link)
- [02_openai_chat](https://colab.research.google.com/drive/1ZVbVT9-KQbgsTaWx9RREUzbQd-GyQ8rz?usp=drive_link)
- [03_stream_chat](https://colab.research.google.com/drive/15fO9pZxVATERvQ6G3JsQAKugEnWS587e?usp=drive_link)
- [04_output_parser](https://colab.research.google.com/drive/1iVzHjd0ks0NkrWWYlknmx3xRRY1Etarb?usp=drive_link)
- [05_lcel_chain](https://colab.research.google.com/drive/1y7_2eeIclEXnJCvq76Lnt8E67-d3DZ7s?usp=drive_link)

### ch04
- [01_prompt_template](https://colab.research.google.com/drive/1idJdPOPZTWEo-fakZ-w-3hY6Z4lbjpxt?usp=drive_link)
- [02_chat_history](https://colab.research.google.com/drive/1ESs73muIOYoOwV1sj0munUbw2BOp8ctA?usp=drive_link)
- [03_prompt_class](https://colab.research.google.com/drive/1iFh1h8uxc8Y4B3aWrOyxI2zji34Xxkr0?usp=drive_link)

### ch05
- [01_embedding](https://colab.research.google.com/drive/1gtLoi-JbTWI0lY_so1VWnJtau-1PjBgD?usp=drive_link)
- [02_vector_store](https://colab.research.google.com/drive/1Cw_zIl4xY58khV4wynCcIxX3S-Ft4k1-?usp=drive_link)
- [03_rag_news](https://colab.research.google.com/drive/1sk2wHyvjeWHepR1F62LubuVmuBM7fwS2?usp=drive_link)
- [04_rag_pdf](https://colab.research.google.com/drive/1NrLleiSlNteqeA1QFbinGMnIkGhirKju?usp=drive_link)

### ch06
- [01_tracing_project](https://colab.research.google.com/drive/1Ma9TXuGB4aWI48gTs7Ui0NreFk7WpJiC?usp=drive_link)
- [02_langchain_hub](https://colab.research.google.com/drive/1m08RYiWTD6T4XLjrW0ngEyg95DWBlsho?usp=drive_link)
- [03_langsmith_client](https://colab.research.google.com/drive/1HvQL8H3W9q71o_zboot7gczICwJB7b59?usp=drive_link)

### ch07
- [01_agent_with_single_tool](https://colab.research.google.com/drive/1G8aOGbW4A-ESrp9DA322qllxGvgMWaTP?usp=drive_link)
- [02_agent_with_multi_tools](https://colab.research.google.com/drive/1zusIXPlxS6DCBrrmg-imh8kVJSbqRF3G?usp=drive_link)

### ch08
- [01_basic_chatbot_graph](https://colab.research.google.com/drive/1ykdoFeBCTeYhRCZ-zhO3OCb9oPhIqQS2?usp=drive_link)
- [02_add_tools](https://colab.research.google.com/drive/1yNsVUE52f7HaJl3_rH8yug6EDnQajuvq?usp=drive_link)
- [03_human_in_the_loop](https://colab.research.google.com/drive/12NY85AIpmHrhs5VspoF9bQ53R4QshONt?usp=drive_link)
- [04_multi_agent](https://colab.research.google.com/drive/1JWXJtnUQLUoMRPjfYkGG-iksMxb9_zOr?usp=drive_link)

### ch09
- [01_mcp_agent](https://colab.research.google.com/drive/1fEWiYHH_GtY_aJdKA3hYNVH7oGvOf-C2?usp=drive_link)

### ch10
- [01_mcp_agent_notion](https://colab.research.google.com/drive/1imW5JpO7FGOFLip7mWxZ7pHHIf60cfb9?usp=drive_link)
- [02_mcp_agent_geeknews](https://colab.research.google.com/drive/1f1_tFv1jsZSWLxDz6oN2siGVfnkTMwMa?usp=drive_link)

### ch11
- [01_meeting_note_pipeline](https://colab.research.google.com/drive/18DWO81Du1VmWGFS7dodrmc5maU9XmV0U?usp=drive_link)

## 📄 라이선스

이 프로젝트는 교육 목적으로 제공되며, 각 챕터의 LICENSE 파일을 참고하세요.