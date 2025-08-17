"""파일 출력 처리 모듈"""

from pathlib import Path
from typing import Any, Dict


class FileHandler:
    """회의록 결과를 파일로 저장하는 핸들러"""
    
    def __init__(self) -> None:
        """파일 핸들러 초기화"""
        pass
    
    def save_meeting_notes(
        self, 
        result: Dict[str, Any], 
        output_path: str = None,
        verbose: bool = True
    ) -> str:
        """회의록 결과를 마크다운 파일로 저장
        
        Args:
            result: 전사 및 요약 결과 딕셔너리
            output_path: 결과 저장 경로 (None이면 자동 생성)
            verbose: 진행 메시지 출력 여부
            
        Returns:
            저장된 출력 파일 경로
        """
        # 1. 출력 경로 설정
        if output_path is None:
            audio_file = Path(result['audio_file'])
            output_path = audio_file.parent / f"{audio_file.stem}_notes.md"
        
        output_file = Path(output_path)
        
        # 2. 마크다운 형식으로 내용 구성
        content = f"""# 회의록

**음성 파일:** {result['audio_file']}  
**전사 길이:** {result['character_count']} 글자

## 원본 전사 내용

{result['transcript']}

## 요약

{result['summary']}
"""
        
        # 3. 파일 저장
        output_file.write_text(content, encoding='utf-8')
        
        if verbose:
            print(f"결과가 저장되었습니다: {output_file}")
            
        return str(output_file)
    
    def create_result_dict(
        self, 
        transcript: str, 
        summary: str, 
        audio_file: str
    ) -> Dict[str, Any]:
        """결과 딕셔너리 생성
        
        Args:
            transcript: 전사 텍스트
            summary: 요약 텍스트
            audio_file: 음성 파일 경로
            
        Returns:
            결과 딕셔너리
        """
        return {
            "transcript": transcript,
            "summary": summary,
            "audio_file": str(audio_file),
            "character_count": len(transcript)
        }