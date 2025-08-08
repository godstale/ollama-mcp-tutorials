import argparse

from pipeline import MeetingNotesPipeline


def main():
    # 1. 명령행 인자 설정
    parser = argparse.ArgumentParser(description="AI 기반 회의록 생성 시스템")
    parser.add_argument(
        "--audio_path", 
        default="meeting_audio_sample.mp3", 
        help="회의 오디오 파일 경로 (mp3/wav)"
    )
    
    args = parser.parse_args()
    
    # 2. 파이프라인 실행
    pipeline = MeetingNotesPipeline()
    pipeline.run(args.audio_path)


if __name__ == "__main__":
    main()