# Meeting Notes Pipeline

AI 기반 회의록 자동 생성 시스템

## 개요

음성 파일을 텍스트로 변환하고 LLM을 활용하여 구조화된 회의록을 자동 생성하는 파이프라인입니다.

### 주요 기능
- **음성 전사**: Faster Whisper를 사용한 고품질 한국어 음성 인식
- **지능형 요약**: Ollama LLM을 활용한 구조화된 회의록 생성
- **다양한 출력**: 콘솔 출력 및 마크다운 파일 저장 지원
- **유연한 설정**: 모델 크기 및 LLM 선택 가능

## 빠른 시작

### 1. 요구사항
- Python 3.10+
- [Ollama](https://ollama.ai/) 설치 필요

### 2. 설치
```bash
# 저장소 클론
git clone <repository-url>
cd ch10

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

## 프로젝트 구조

```
ch10/
├── src/
│   └── meeting_notes/           # 메인 패키지
│       ├── __init__.py         # 패키지 초기화
│       ├── transcriber.py      # 음성 전사 모듈
│       ├── summarizer.py       # LLM 요약 모듈
│       └── pipeline.py         # 메인 파이프라인
├── assets/
│   └── meeting_audio_sample.mp3 # 샘플 오디오 파일
├── main.py                     # CLI 진입점
├── pyproject.toml             # 프로젝트 설정
├── .gitignore                 # Git 무시 파일
└── README.md                  # 프로젝트 문서
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
from src.meeting_notes import MeetingNotesPipeline

# 파이프라인 초기화
pipeline = MeetingNotesPipeline(
    model_size="base",
    llm_model="qwen3:8b"
)

# 처리 실행
result = pipeline.run("path/to/audio.mp3")
print(result["summary"])

# 파일로 저장
output_file = pipeline.process_and_save(
    "path/to/audio.mp3",
    "output/meeting_notes.md"
)
```

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