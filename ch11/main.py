#!/usr/bin/env python3
"""회의록 생성기 - AI 기반 회의록 자동 생성을 위한 CLI 인터페이스"""

import argparse

from src import MeetingNotesPipeline


def main() -> None:
    """회의록 생성을 위한 CLI 진입점"""
    # 1. 명령행 인자 설정
    parser = argparse.ArgumentParser(
        description="AI 기반 회의록 자동 생성 시스템"
    )
    
    parser.add_argument(
        "--audio-path",
        type=str,
        default="assets/meeting_audio_sample.mp3",
        help="회의 오디오 파일 경로 (mp3/wav)"
    )
    
    parser.add_argument(
        "--model-size", 
        type=str,
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper 모델 크기 선택"
    )
    
    parser.add_argument(
        "--llm-model",
        type=str, 
        default="qwen3:8b",
        help="요약에 사용할 LLM 모델명"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="결과 저장 파일 경로 (기본값: 자동 생성)"
    )
    
    
    args = parser.parse_args()
    
    try:
        # 2. 파이프라인 초기화
        pipeline = MeetingNotesPipeline(
            model_size=args.model_size,
            llm_model=args.llm_model
        )
        
        # 3. 처리 실행
        pipeline.run(args.audio_path)
            
    except FileNotFoundError as e:
        print(f"[오류] 파일을 찾을 수 없습니다: {e}")
    except Exception as e:
        print(f"[오류] 오류가 발생했습니다: {str(e)}")


if __name__ == "__main__":
    main()