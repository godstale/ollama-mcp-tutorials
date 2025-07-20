import os
from dotenv import load_dotenv
from langsmith import Client
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# 1. 환경 변수 로드
load_dotenv()
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

# 2. 랭스미스 클라이언트트 초기화 및 프롬프트 불러오기
client = Client(api_key=LANGSMITH_API_KEY)
prompt = client.pull_prompt("hardkothari/prompt-maker", include_model=False)

# 3. 간단한 원본 프롬프트와 요청
short_prompt = "LLM는 무엇인가?"
task = "한국어로 구체적으로 질문에 대한 프롬프트를 작성해주세요."

# 4. 올라마 모델 초기화
llm = ChatOllama(model="qwen3:8b", temperature=0)

# 5. 프롬프트 템플릿에 변수 주입하여 메시지 생성
messages = prompt.invoke({
    "task": task,
    "lazy_prompt": short_prompt
})

# 6. HumanMessage에서 실제 사용자 프롬프트 텍스트만 추출
user_prompt = [m.content for m in messages.messages if isinstance(m, HumanMessage)][0]

# 7. LLM 실행
response = llm.invoke(user_prompt)

# 8. 결과과 출력
print("원본 프롬프트:", short_prompt)
print("개선된 프롬프트:\n")
print(response.content)