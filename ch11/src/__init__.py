"""회의록 파이프라인 - AI 기반 회의록 자동 생성 시스템"""

__version__ = "0.1.0"

from pipeline import MeetingNotesPipeline
from summarizer import MeetingSummarizer
from transcriber import AudioTranscriber

__all__ = [
    "AudioTranscriber",
    "MeetingSummarizer", 
    "MeetingNotesPipeline"
]