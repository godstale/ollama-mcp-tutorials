"""LangGraph 기반 회의록 파이프라인 - 워크플로우로 전사, 요약, 파일 저장 관리"""

import os
from pathlib import Path
from typing import Annotated, Any, Dict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from file_handler import FileHandler
from summarizer import MeetingSummarizer
from transcriber import AudioTranscriber


class MeetingState(TypedDict):
    """회의록 처리 워크플로우 상태"""
    audio_path: str
    transcript: str
    summary: str
    result: Dict[str, Any]
    output_path: str
    verbose: bool


class MeetingNotesPipeline:
    """LangGraph 기반 음성에서 회의록 생성까지 전체 파이프라인"""
    
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
        self.file_handler = FileHandler()
        
        # LangGraph 워크플로우 구성
        self.graph = self._build_workflow()
        
        # 그래프 시각화 생성
        self._save_graph_visualization()
    
    def _build_workflow(self) -> StateGraph:
        """LangGraph 워크플로우 구성"""
        # 1. 그래프 빌더 생성
        graph_builder = StateGraph(MeetingState)
        
        # 2. 노드 추가
        graph_builder.add_node("validate_input", self._validate_input_node)
        graph_builder.add_node("transcribe", self._transcribe_node)
        graph_builder.add_node("summarize", self._summarize_node)
        graph_builder.add_node("save_file", self._save_file_node)
        
        # 3. 엣지 추가 (순차 실행)
        graph_builder.add_edge(START, "validate_input")
        graph_builder.add_edge("validate_input", "transcribe")
        graph_builder.add_edge("transcribe", "summarize")
        graph_builder.add_edge("summarize", "save_file")
        graph_builder.add_edge("save_file", END)
        
        # 4. 그래프 컴파일
        return graph_builder.compile()
    
    def _save_graph_visualization(self) -> None:
        """LangGraph 워크플로우 구조를 PNG로 저장"""
        try:
            # 그래프를 PNG 파일로 저장
            png_data = self.graph.get_graph(xray=True).draw_mermaid_png()
            
            # 현재 작업 디렉토리에 'graph.png' 파일로 저장
            file_path = os.path.join(os.getcwd(), "graph.png")
            with open(file_path, "wb") as f:
                f.write(png_data)
            print(f"[시각화] 워크플로우 구조 저장: {file_path}")
            
        except Exception as e:
            print(f"[경고] 그래프 시각화 생성 실패: {e}")
    
    def _validate_input_node(self, state: MeetingState) -> MeetingState:
        """입력 파일 검증 노드"""
        audio_file = Path(state["audio_path"])
        if not audio_file.exists():
            raise FileNotFoundError(f"음성 파일을 찾을 수 없습니다: {audio_file}")
        
        if state["verbose"]:
            print(f"[검증] 음성 파일 확인 완료: {audio_file.name}")
        
        return state
    
    def _transcribe_node(self, state: MeetingState) -> MeetingState:
        """음성 전사 노드"""
        if state["verbose"]:
            print("[1단계] 음성을 텍스트로 변환 중...")
            
        transcript = self.transcriber.transcribe(state["audio_path"])
        
        if state["verbose"]:
            print(f"변환 완료! ({len(transcript)} 글자)")
            print(transcript)
        
        # 상태 업데이트
        state["transcript"] = transcript
        return state
    
    def _summarize_node(self, state: MeetingState) -> MeetingState:
        """요약 생성 노드"""
        if state["verbose"]:
            print("\n[2단계] 회의록 요약 생성 중...")
            
        summary = self.summarizer.summarize(state["transcript"])
        
        if state["verbose"]:
            print("요약 완료!")
            print(summary)
        
        # 상태 업데이트
        state["summary"] = summary
        return state
    
    def _save_file_node(self, state: MeetingState) -> MeetingState:
        """파일 저장 노드"""
        if state["verbose"]:
            print("\n[3단계] 파일 저장 중...")
        
        # 결과 딕셔너리 생성
        result = self.file_handler.create_result_dict(
            transcript=state["transcript"],
            summary=state["summary"],
            audio_file=state["audio_path"]
        )
        
        # 파일 저장 - output_path가 빈 문자열이면 None으로 처리
        output_path_arg = state.get("output_path")
        if not output_path_arg:
            output_path_arg = None
            
        output_path = self.file_handler.save_meeting_notes(
            result=result,
            output_path=output_path_arg,
            verbose=state["verbose"]
        )
        
        if state["verbose"]:
            print("\n[완료] 회의록 생성이 완료되었습니다!")
        
        # 상태 업데이트
        state["result"] = result
        state["output_path"] = output_path
        return state
    
    def run(
        self, 
        audio_path: str, 
        output_path: str = None,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """전체 파이프라인 실행: 전사 → 요약 → 파일 저장
        
        Args:
            audio_path: 음성 파일 경로
            output_path: 결과 저장 경로 (None이면 자동 생성)
            verbose: 진행 메시지 출력 여부
            
        Returns:
            전사 내용, 요약, 저장된 파일 경로를 포함한 딕셔너리
            
        Raises:
            FileNotFoundError: 음성 파일이 존재하지 않을 경우
        """
        # 초기 상태 구성
        initial_state = MeetingState(
            audio_path=audio_path,
            transcript="",
            summary="",
            result={},
            output_path=output_path or "",
            verbose=verbose
        )
        
        # 워크플로우 실행
        final_state = self.graph.invoke(initial_state)
        
        # 결과에 출력 경로 추가
        result = final_state["result"].copy()
        result["output_path"] = final_state["output_path"]
        
        return result