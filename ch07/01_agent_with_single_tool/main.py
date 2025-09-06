from dotenv import load_dotenv
from langchain.agents import Tool
from langchain.agents.agent import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


# 환경 변수 로드 (.env 파일에서 API 키 등을 로드)
load_dotenv()

# 1. ReAct 에이전트를 위한 프롬프트 템플릿 생성
prompt = ChatPromptTemplate.from_template(
    """당신은 유능한 기상학자입니다. 온도에 대한 답변은 섭씨로 해주세요. 필요한 경우 다음 도구들을 사용할 수 있습니다: 
    {tools}

    Important: You must strictly follow the format below. The Final Answer should only appear after a Thought. If no Action is needed, do not skip it or write that you're proceeding without an action — always adhere to the structure.

    Use the following format:
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Chat history: {chat_history}
    Question: {question}
    Thought:{agent_scratchpad}
    """
)

# 2. Ollama 초기화
llm = ChatOllama(
    model="qwen3:8b",
    temperature=0,
)

# 3. 에이전트가 사용할 도구들 초기화
# 3-1. Tavily 검색 도구: 웹 검색을 수행
search_tool = Tool(
    name="WebSearch",
    func=TavilySearchResults().run,
    description="This is a real-time web search tool (based on Tavily service)",
)

# 3-2. 도구 리스트 생성
tools = [search_tool]

# 4. ReAct 에이전트 생성 및 실행기 설정
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)

# 5. 대화 기록을 저장할 리스트 초기화
chat_history = []

# 6. 대화 루프 실행
print("기상학자 AI와 대화를 시작합니다.")

while True:
    # 6-1. 사용자 입력 받기
    user_input = input("질문을 입력하세요 (종료: exit): ")
    if user_input.lower() == "exit":
        break

    try:
        # 6-2. 에이전트 실행 및 응답 생성
        result = agent_executor.invoke(
            {"question": user_input, "chat_history": chat_history}
        )

        # 6-3. 응답 출력
        output_text = result["output"]
        print(f"\nAI --->\n{output_text}")

        # 6-4. 대화 기록에 현재 대화 추가
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=output_text))

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
