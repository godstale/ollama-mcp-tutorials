from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import AIMessage, HumanMessage
from langchain_tavily import TavilySearch
from langchain_ollama import ChatOllama


# .env 파일에서 API 키와 같은 환경 변수를 로드합니다.
load_dotenv()

# 1. 간단한 시스템 프롬프트를 정의합니다.
# create_agent가 내부적으로 ReAct 로직을 처리하므로 복잡한 템플릿이 필요 없습니다.
SYSTEM_PROMPT = "당신은 유능한 기상학자입니다. 온도에 대한 답변은 섭씨로 해주세요. 사용자가 대화에서 벗어나면, 정중하게 대화를 날씨 관련 주제로 다시 유도해주세요."

# 2. 언어 모델(LLM)을 초기화합니다.
# 여기서는 qwen3:8b 모델을 사용하는 Ollama를 설정합니다.
llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
)

# 3. 에이전트가 사용할 도구를 초기화합니다.
# TavilySearch를 직접 도구 목록에 추가합니다.
tools = [TavilySearch(max_results=2)]

# 4. LangChain v1 스타일의 에이전트를 생성합니다.
# create_agent는 실행 가능한(runnable) 에이전트를 반환합니다.
agent = create_agent(llm, tools, system_prompt=SYSTEM_PROMPT)

# 5. 대화 기록을 저장할 리스트를 초기화합니다.
chat_history = []

print("기상학자 AI와 대화를 시작합니다. 'exit'를 입력하면 종료됩니다.")

while True:
    user_input = input("질문: ")
    if user_input.lower() == "exit":
        break

    try:
        # 6. 대화 기록과 사용자 입력을 포함하여 에이전트를 실행합니다.
        # create_agent는 'messages' 키에 메시지 리스트를 담은 딕셔너리를 입력으로 받습니다.
        response = agent.invoke(
            {
                "messages": chat_history + [HumanMessage(content=user_input)],
            }
        )

        # 7. AI의 응답을 출력합니다.
        ai_message = response["messages"][-1]
        if isinstance(ai_message, AIMessage):
            print(f"\nAI: {ai_message.content}")
            # 8. 대화 기록을 업데이트합니다.
            chat_history.extend(
                [
                    HumanMessage(content=user_input),
                    AIMessage(content=ai_message.content),
                ]
            )

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
