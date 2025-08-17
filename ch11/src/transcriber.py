"""Faster Whisper를 사용한 음성 전사 모듈"""

from pathlib import Path
from typing import Optional

from faster_whisper import WhisperModel


class AudioTranscriber:
    """Faster Whisper를 사용한 음성-텍스트 변환"""
    
    def __init__(
        self, 
        model_size: str = "base",
        device: str = "cpu",
        compute_type: str = "int8"
    ) -> None:
        """설정된 모델 구성으로 전사기 초기화
        
        Args:
            model_size: Whisper 모델 크기 ("tiny", "base", "small", "medium", "large")
            device: 실행할 장치 ("cpu")
            compute_type: 계산 정밀도 ("int8", "int16", "float16", "float32")
        """
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self._model: Optional[WhisperModel] = None
    
    def _load_model(self) -> None:
        """Whisper 모델이 로드되지 않았다면 로드"""
        if self._model is None:
            print(f"Faster Whisper 모델 로딩 중: {self.model_size}")
            self._model = WhisperModel(
                self.model_size, 
                device=self.device, 
                compute_type=self.compute_type
            )
    
    def transcribe(self, audio_path: str, language: str = "ko") -> str:
        """음성 파일을 텍스트로 변환
        
        Args:
            audio_path: 음성 파일 경로
            language: 전사에 사용할 언어 코드
            
        Returns:
            변환된 텍스트
            
        Raises:
            FileNotFoundError: 음성 파일이 존재하지 않을 경우
        """
        # 1. 파일 경로 검증
        audio_file = Path(audio_path)
        if not audio_file.exists():
            raise FileNotFoundError(f"음성 파일을 찾을 수 없습니다: {audio_file}")
        
        # 2. 모델 로드
        self._load_model()
        
        # 3. 음성 파일 변환 시작
        print(f"음성 파일 변환 중: {audio_file.name}")
        print(f"사용 모델: {self.model_size}")
        
        # 4. 전사 실행
        segments, _ = self._model.transcribe(str(audio_file), language=language)
        
        # 5. 세그먼트들을 하나의 텍스트로 결합
        transcript = "".join(segment.text for segment in segments)
        
        print("음성 변환 완료!")
        return transcript.strip()