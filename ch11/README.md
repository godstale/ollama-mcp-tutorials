# Meeting Notes Pipeline

AI 기반 회의록 자동 생성 시스템 (LangGraph 워크플로우 기반)

## 개요

**LangGraph 워크플로우**를 사용하여 음성 파일을 텍스트로 변환하고 LLM을 활용하여 구조화된 회의록을 자동 생성하는 파이프라인입니다.

### 주요 기능
- **LangGraph 워크플로우**: 상태 기반 그래프 실행으로 처리 단계 관리
- **모듈화 설계**: 독립적인 전사, 요약, 파일 처리 컴포넌트
- **음성 전사**: Faster Whisper를 사용한 고품질 한국어 음성 인식
- **지능형 요약**: Ollama LLM을 활용한 구조화된 회의록 생성
- **다양한 출력**: 콘솔 출력 및 마크다운 파일 저장 지원
- **유연한 설정**: 모델 크기 및 LLM 선택 가능
- **워크플로우 시각화**: 그래프 구조를 PNG 파일로 자동 생성

## 빠른 시작

### 1. 요구사항
- Python 3.10+
- [Ollama](https://ollama.ai/) 설치 필요

### 2. 설치
```bash
# 저장소 클론
git clone <repository-url>
cd ch11

# 의존성 설치
uv sync
```

### 3. Ollama 모델 설치
```bash
ollama pull qwen3:8b
```

### 4. 실행
```bash
# 기본 실행 (샘플 파일 사용)
uv run python main.py

# 특정 파일 처리
uv run python main.py --audio-path path/to/your/audio.mp3

# 결과를 파일로 저장
uv run python main.py --audio-path path/to/audio.mp3 --save

# 고급 옵션
uv run python main.py \\
  --audio-path path/to/audio.mp3 \\
  --model-size base \\
  --llm-model qwen3:8b \\
  --save
```

## 아키텍처 및 리팩토링 개요

### LangGraph 워크플로우 기반 설계

이 프로젝트는 **LangGraph**를 사용하여 상태 기반 워크플로우로 리팩토링되었습니다. 각 처리 단계가 독립적인 노드로 구성되어 있어 명확한 데이터 흐름과 상태 관리를 제공합니다.

#### 워크플로우 단계
1. **validate_input**: 입력 오디오 파일 검증
2. **transcribe**: Faster Whisper를 사용한 음성-텍스트 변환  
3. **summarize**: Ollama LLM을 사용한 구조화된 요약 생성
4. **save_file**: 결과를 마크다운 파일로 저장

#### 주요 리팩토링 사항
- **모듈 분리**: 각 기능별로 독립적인 모듈 (`transcriber.py`, `summarizer.py`, `file_handler.py`)
- **상태 관리**: `MeetingState` TypedDict로 워크플로우 상태 정의
- **에러 처리**: 각 노드에서 예외 처리 및 상태 전파
- **시각화**: 워크플로우 구조를 자동으로 PNG 파일 생성

### 프로젝트 구조

```
ch11/
├── src/
│   ├── __init__.py            # 패키지 초기화 및 exports
│   ├── pipeline.py            # LangGraph 워크플로우 메인 파이프라인
│   ├── transcriber.py         # Faster Whisper 음성 전사 모듈
│   ├── summarizer.py          # Ollama LLM 요약 모듈
│   └── file_handler.py        # 파일 저장 및 결과 처리 모듈
├── assets/
│   ├── meeting_audio_sample.mp3 # 샘플 오디오 파일
│   └── meeting_audio_sample_notes.md # 샘플 결과 파일
├── main.py                    # CLI 진입점
├── pyproject.toml            # 프로젝트 설정 및 의존성
├── coding_rules.md           # 코딩 스타일 가이드 (한국어)
├── graph.png                 # 자동 생성된 워크플로우 시각화
└── README.md                 # 프로젝트 문서
```

## 사용법

### CLI 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--audio-path` | 처리할 오디오 파일 경로 | `assets/meeting_audio_sample.mp3` |
| `--model-size` | Whisper 모델 크기 | `base` |
| `--llm-model` | 요약에 사용할 LLM 모델 | `qwen3:8b` |
| `--output` | 출력 파일 경로 (--save 사용시) | 자동 생성 |
| `--save` | 결과를 파일로 저장 | False |

### Python 코드에서 사용

```python
from src import MeetingNotesPipeline

# LangGraph 파이프라인 초기화
pipeline = MeetingNotesPipeline(
    model_size="base",
    llm_model="qwen3:8b"
)

# 워크플로우 실행 (콘솔 출력)
result = pipeline.run("path/to/audio.mp3")
print(result["summary"])

# 워크플로우 실행 후 파일 저장
output_file = pipeline.process_and_save(
    "path/to/audio.mp3",
    "output/meeting_notes.md"
)
print(f"저장된 파일: {output_file}")

# 그래프 시각화는 자동으로 graph.png에 저장됨
```

### LangGraph 워크플로우 특징

- **상태 기반 실행**: 각 단계의 상태가 `MeetingState`에 저장되어 추적 가능
- **에러 복구**: 각 노드에서 발생하는 에러를 적절히 처리
- **병렬 처리 가능**: 필요시 독립적인 작업을 병렬로 실행 가능한 구조
- **확장성**: 새로운 처리 단계를 노드로 쉽게 추가 가능

## 출력 형식

생성된 회의록은 다음과 같은 구조를 가집니다:

```markdown
### 1. 주요 논의 사항
- 논의된 핵심 포인트들

### 2. 결정된 사항
- 회의에서 결정된 내용들

### 3. 액션 아이템
- 후속 조치나 다음 단계들
```