# MCP Agent

MCP(Model Context Protocol)를 사용한 에이전트 예제입니다.

## 설명

이 예제는 MCP(Model Context Protocol)를 활용하여 외부 서비스와 연결된 에이전트 시스템을 구현합니다. MCP 서버를 통해 날씨 정보 등의 실시간 데이터에 접근할 수 있습니다.

## 주요 구성 요소

- **MCP Client**: MCP 프로토콜 클라이언트
- **MCP Server**: 날씨 정보 제공 서버
- **Agent Integration**: MCP 도구를 사용하는 에이전트

## 프로젝트 구조

```
ch09/01_mcp_agent/
├── main.py              # 메인 애플리케이션
├── mcp_manager.py       # MCP 클라이언트 관리
├── mcp_prompt.py        # MCP 관련 프롬프트
├── mcp_config.json      # MCP 서버 설정
└── mcp_server/
    └── mcp_server_weather.py  # 날씨 MCP 서버
```

## 사전 요구 사항

1. Ollama 설치 및 실행
2. OpenAI API 키 (권장, MCP 도구 사용을 위해)
3. 환경 변수 설정:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

## 실행 방법

1. 프로젝트 디렉토리로 이동:
   ```bash
   cd ch09/01_mcp_agent
   ```

2. 의존성 설치:
   ```bash
   uv sync
   ```

3. 프로그램 실행:
   ```bash
   uv run main.py
   ```

4. MCP 도구를 활용한 질문을 입력하세요.

## MCP 설정

`mcp_config.json` 파일에서 MCP 서버 설정을 확인하고 필요시 수정할 수 있습니다.

## 그래프 구조 확인

프로젝트 디렉토리에 `graph.png` 파일이 생성되어 MCP 에이전트 시스템의 구조를 시각적으로 확인할 수 있습니다.