from faster_whisper import WhisperModel
from pathlib import Path


class AudioTranscriber:
    """음성 파일을 텍스트로 변환하는 클래스 (Faster Whisper 사용)"""
    
    def __init__(self, model_size: str = "base"):
        self.model_size = model_size
        self.model = None
    
    def _load_model(self):
        """Faster Whisper 모델을 로드합니다."""
        if self.model is None:
            print(f"Faster Whisper 모델 로딩 중... (모델: {self.model_size})")
            self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
    
    def transcribe(self, audio_path: str) -> str:
        """음성 파일을 텍스트로 변환합니다."""
        
        # 1. 파일 경로 검증
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"음성 파일을 찾을 수 없습니다: {audio_path}")
        
        # 2. 모델 로드
        self._load_model()
        
        # 3. 음성 파일 변환
        print(f"음성 파일 변환 중: {audio_path.name}")
        print(f"사용 모델: {self.model_size}")
        
        segments, info = self.model.transcribe(str(audio_path), language="ko")
        
        # 4. 세그먼트들을 하나의 텍스트로 합치기
        transcript = ""
        for segment in segments:
            transcript += segment.text
        
        print("음성 변환 완료!")
        return transcript