from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import AIMessage, HumanMessage
from langchain.tools import tool, BaseTool
from langchain_tavily import TavilySearchResults
from langchain_classic.chains.llm_math.base import LLMMathChain
from langchain_ollama import ChatOllama


# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# 1. 시스템 프롬프트를 정의합니다. create_agent가 ReAct 로직을 처리하므로 간단하게 작성합니다.
SYSTEM_PROMPT = "당신은 여러 도구를 사용하여 질문에 답할 수 있는 유능한 AI 어시스턴트입니다. 명확하고 간결하게 답변해주세요."

# 2. 언어 모델(LLM)을 초기화합니다.
llm = ChatOllama(model="qwen3:8b", temperature=0)

# 3. 에이전트가 사용할 도구들을 정의합니다.
# 3-1. Tavily 검색 도구
search_tool = TavilySearchResults(max_results=2)

# 3-2. 수학 계산 도구 (langchain-classic의 LLMMathChain 사용)
math_chain = LLMMathChain.from_llm(llm=llm)

@tool
def math_calculator(expression: str) -> str:
    """수학 관련 질문에 답변할 때 유용합니다.
    이 도구는 수학 문제 전용입니다.
    수학적 표현식만 입력하세요."""
    return math_chain.run(expression)


# 3-3. 파일 저장 도구 (@tool 데코레이터 사용)
@tool
def save_to_file_tool(text: str) -> str:
    """주어진 텍스트를 'output.txt' 파일에 저장합니다."""
    with open("output.txt", "w") as f:
        print("파일에 저장 중: output.txt")
        f.write(text)
    return "파일 저장 완료"


# 3-4. 도구 리스트를 생성합니다.
tools = [search_tool, math_calculator, save_to_file_tool]

# 4. LangChain v1 스타일의 에이전트를 생성합니다.
agent = create_agent(llm, tools, system_prompt=SYSTEM_PROMPT)

# 5. 대화 기록을 저장할 리스트를 초기화합니다.
chat_history = []

print("AI 어시스턴트와 대화를 시작합니다. 'exit'를 입력하면 종료됩니다.")

while True:
    user_input = input("질문: ")
    if user_input.lower() == "exit":
        break

    try:
        # 6. 대화 기록과 사용자 입력을 포함하여 에이전트를 실행합니다.
        response = agent.invoke(
            {
                "messages": chat_history + [HumanMessage(content=user_input)],
            }
        )

        # 7. AI의 응답을 출력하고 대화 기록을 업데이트합니다.
        ai_message = response["messages"][-1]
        if isinstance(ai_message, AIMessage):
            print(f"\nAI: {ai_message.content}")
            chat_history.extend(
                [
                    HumanMessage(content=user_input),
                    AIMessage(content=ai_message.content),
                ]
            )

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
