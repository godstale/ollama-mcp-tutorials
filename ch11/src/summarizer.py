"""LLM을 사용한 회의록 요약 모듈"""

from typing import Optional

from langchain.prompts import PromptTemplate
from langchain_ollama import OllamaLLM


class MeetingSummarizer:
    """LLM을 사용하여 회의록을 구조화된 요약으로 변환"""
    
    def __init__(self, model_name: str = "qwen3:8b") -> None:
        """지정된 LLM 모델로 요약기 초기화
        
        Args:
            model_name: 요약에 사용할 Ollama 모델명
        """
        self.model_name = model_name
        self._llm: Optional[OllamaLLM] = None
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """회의록 요약을 위한 프롬프트 템플릿 생성"""
        template = """다음 회의록을 아래 형식으로 요약해주세요:

### 1. 주요 논의 사항  
- 핵심 포인트들을 bullet point로 정리

### 2. 결정된 사항  
- 결정된 내용들을 bullet point로 정리

### 3. 액션 아이템
- 후속 조치나 다음 단계들을 bullet point로 정리

회의록:
{transcript}"""
        
        return PromptTemplate(
            input_variables=["transcript"],
            template=template
        )
    
    def _load_llm(self) -> None:
        """Ollama LLM 모델이 로드되지 않았다면 로드"""
        if self._llm is None:
            print(f"LLM 모델 로딩 중: {self.model_name}")
            self._llm = OllamaLLM(model=self.model_name)
    
    def summarize(self, transcript: str) -> str:
        """회의록 텍스트에서 구조화된 요약 생성
        
        Args:
            transcript: 회의록 텍스트
            
        Returns:
            구조화된 회의 요약
        """
        # 1. 입력 텍스트 검증
        if not transcript.strip():
            raise ValueError("회의록 텍스트가 비어있습니다")
            
        try:
            # 2. LLM 모델 로드
            self._load_llm()
            
            # 3. 프롬프트 체인 구성 및 실행
            chain = self.prompt_template | self._llm
            summary = chain.invoke({"transcript": transcript})
            
            return summary.strip()
            
        except Exception as e:
            return self._handle_error(e)
    
    def _handle_error(self, error: Exception) -> str:
        """에러 처리 및 사용자 친화적 메시지 반환"""
        error_msg = str(error)
        
        if "404" in error_msg:
            return f"""[오류] 모델을 찾을 수 없습니다: {self.model_name}

다음 명령어로 모델을 설치해주세요:
ollama pull {self.model_name}"""
        else:
            return f"[오류] 요약 생성 중 문제가 발생했습니다: {error_msg}"