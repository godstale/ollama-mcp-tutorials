"""회의록 파이프라인 - 전사와 요약을 통합 관리"""

from pathlib import Path
from typing import Any, Dict

from summarizer import MeetingSummarizer
from transcriber import AudioTranscriber


class MeetingNotesPipeline:
    """음성에서 회의록 생성까지 전체 파이프라인"""
    
    def __init__(
        self, 
        model_size: str = "base",
        llm_model: str = "qwen3:8b"
    ) -> None:
        """지정된 모델들로 파이프라인 초기화
        
        Args:
            model_size: 전사에 사용할 Whisper 모델 크기
            llm_model: 요약에 사용할 LLM 모델명
        """
        self.transcriber = AudioTranscriber(model_size=model_size)
        self.summarizer = MeetingSummarizer(model_name=llm_model)
    
    def run(self, audio_path: str, verbose: bool = True) -> Dict[str, Any]:
        """전체 파이프라인 실행: 전사 → 요약
        
        Args:
            audio_path: 음성 파일 경로
            verbose: 진행 메시지 출력 여부
            
        Returns:
            전사 내용과 요약을 포함한 딕셔너리
            
        Raises:
            FileNotFoundError: 음성 파일이 존재하지 않을 경우
        """
        # 1. 파일 존재 확인
        audio_file = Path(audio_path)
        if not audio_file.exists():
            raise FileNotFoundError(f"음성 파일을 찾을 수 없습니다: {audio_file}")
        
        # 2. 음성을 텍스트로 변환
        if verbose:
            print("[1단계] 음성을 텍스트로 변환 중...")
            
        transcript = self.transcriber.transcribe(audio_path)
        
        if verbose:
            print(f"변환 완료! ({len(transcript)} 글자)")
            print(transcript)
        
        # 3. 구조화된 요약 생성
        if verbose:
            print("\n[2단계] 회의록 요약 생성 중...")
            
        summary = self.summarizer.summarize(transcript)
        
        if verbose:
            print("요약 완료!")
            print(summary)
            print("\n[완료] 회의록 생성이 완료되었습니다!")
        
        return {
            "transcript": transcript,
            "summary": summary,
            "audio_file": str(audio_file),
            "character_count": len(transcript)
        }
    
    def process_and_save(
        self, 
        audio_path: str, 
        output_path: str = None,
        verbose: bool = True
    ) -> str:
        """음성 처리 후 결과를 파일로 저장
        
        Args:
            audio_path: 음성 파일 경로
            output_path: 결과 저장 경로 (None이면 자동 생성)
            verbose: 진행 메시지 출력 여부
            
        Returns:
            저장된 출력 파일 경로
        """
        # 1. 파이프라인 실행
        result = self.run(audio_path, verbose)
        
        # 2. 출력 경로 설정
        if output_path is None:
            audio_file = Path(audio_path)
            output_path = audio_file.parent / f"{audio_file.stem}_notes.md"
        
        output_file = Path(output_path)
        
        # 3. 마크다운 형식으로 내용 구성
        content = f"""# 회의록

**음성 파일:** {result['audio_file']}  
**전사 길이:** {result['character_count']} 글자

## 원본 전사 내용

{result['transcript']}

## 요약

{result['summary']}
"""
        
        # 4. 파일 저장
        output_file.write_text(content, encoding='utf-8')
        
        if verbose:
            print(f"결과가 저장되었습니다: {output_file}")
            
        return str(output_file)