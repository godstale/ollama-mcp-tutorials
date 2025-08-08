import os

from audio_transcriber import AudioTranscriber
from meeting_summarizer import MeetingSummarizer


class MeetingNotesPipeline:
    """회의 오디오를 텍스트로 변환하고 요약하는 파이프라인"""
    
    def __init__(self):
        self.transcriber = AudioTranscriber()
        self.summarizer = MeetingSummarizer()
    
    def run(self, audio_path: str) -> None:
        """파이프라인 실행: 음성변환 → 요약 → 결과출력"""
        
        # 1. 파일 존재 확인
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {audio_path}")
        
        # 2. 음성을 텍스트로 변환
        print("[1단계] 음성을 텍스트로 변환중...")
        transcript = self.transcriber.transcribe(audio_path)
        print(f"변환 완료! 총 {len(transcript)} 글자")
        print(transcript)
        
        # 3. 텍스트를 구조화된 회의록으로 요약
        print("\n[2단계] 회의록 요약 생성중...")
        summary = self.summarizer.summarize(transcript)
        print("요약 완료!")
        print(summary)
        
        print("\n[완료] 회의록 생성이 완료되었습니다!")