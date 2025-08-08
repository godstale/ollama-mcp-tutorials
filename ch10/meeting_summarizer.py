from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate


class MeetingSummarizer:
    """회의 텍스트를 구조화된 요약으로 변환하는 클래스"""
    
    def __init__(self, model_name: str = "qwen3:8b"):
        self.model_name = model_name
        self.llm = None
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self) -> PromptTemplate:
        """회의록 요약을 위한 프롬프트 템플릿을 생성합니다"""
        template = """다음 회의록을 아래 형식으로 요약해주세요:

1. 주요 논의 사항
- 핵심 포인트들을 bullet point로 정리

2. 결정된 사항  
- 결정된 내용들을 bullet point로 정리

3. 액션 아이템
- 후속 조치나 다음 단계들을 bullet point로 정리

회의록:
{transcript}"""
        
        return PromptTemplate(
            input_variables=["transcript"],
            template=template
        )
    
    def _load_llm(self):
        """Ollama LLM 모델을 로드합니다"""
        if self.llm is None:
            print(f"LLM 모델 로딩중: {self.model_name}")
            self.llm = OllamaLLM(model=self.model_name)
    
    def summarize(self, transcript: str) -> str:
        """회의 텍스트를 구조화된 요약으로 변환합니다"""
        
        try:
            # 1. LLM 모델 로드
            self._load_llm()
            
            # 2. 프롬프트 체인 구성
            chain = self.prompt_template | self.llm
            
            # 3. 요약 생성
            summary = chain.invoke({"transcript": transcript})
            
            return summary.strip()
            
        except Exception as e:
            return self._handle_error(e)
    
    def _handle_error(self, error: Exception) -> str:
        """에러 처리 및 사용자 친화적 메시지 반환"""
        error_msg = str(error)
        
        if "404" in error_msg:
            return f"""[ERROR] 모델을 찾을 수 없습니다: {self.model_name}

다음 명령어로 모델을 설치해주세요:
ollama pull {self.model_name}"""
        else:
            return f"[ERROR] 요약 생성 중 오류가 발생했습니다: {error_msg}"