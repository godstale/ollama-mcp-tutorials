import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI
from langchain.agents.react.agent import create_react_agent
from langchain.chains.llm_math.base import LLMMathChain
from langchain.agents import Tool
from langchain.agents.agent import AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage

# 환경 변수 로드 (.env 파일에서 API 키 등을 로드)
load_dotenv()

# 1. ReAct 에이전트를 위한 프롬프트 템플릿 생성
# ReAct는 Reasoning + Acting의 약자로, 추론과 행동을 반복하며 문제를 해결하는 방식입니다.
prompt = ChatPromptTemplate.from_template(
    """
    Answer the following questions as best you can.
    You have access to the following tools:
    {tools}

    Use the following format:
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    ============================= Chat history =============================
    {chat_history}
    ================================ Human Message =================================
    Question: {question}
    ============================= Messages Placeholder =============================
    Thought:{agent_scratchpad}
    """
)

# 2. OpenAI의 Chat 모델 초기화
# temperature=0으로 설정하여 일관된 응답을 생성하도록 합니다.
llm = ChatOpenAI(
    temperature=0,
    model_name="gpt-4.1-mini",
)

# 3. 에이전트가 사용할 도구들 초기화
# 3-1. DuckDuckGo 검색 도구: 웹 검색을 수행
search_tool = Tool(
    name="Search",
    func=DuckDuckGoSearchRun().run,
    description="DuckDuckGo 웹 검색 도구"
)

# 3-2. 수학 계산 도구: 수학적 계산을 수행
math_tool = Tool.from_function(
    name="Calculator",
    func=LLMMathChain.from_llm(llm=llm).run,
    description="""Useful for when you need to answer questions about math.
        This tool is only for math questions and nothing else.
        Only input math expressions.""",
)

# 3-3. 도구 리스트 생성
tools = [search_tool, math_tool]

# 4. ReAct 에이전트와 실행기 생성
# verbose=True로 설정하여 에이전트의 추론 과정을 출력합니다.
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

# 5. 대화 기록을 저장할 리스트 초기화
chat_history = []

# 6. 대화 루프 실행
while True:
    # 6-1. 사용자 입력 받기
    user_input = input("질문을 입력하세요 (종료: exit): ")
    if user_input.lower() == "exit":
        break

    # 6-2. 에이전트 실행 및 응답 생성
    # chat_history를 포함하여 이전 대화 맥락을 유지합니다.
    result = agent_executor.invoke(
        {"question": user_input, "chat_history": chat_history}
    )
    output_text = result["output"]
    print(f"\nAI --->\n{output_text}")

    # 6-3. 대화 기록 업데이트
    # 사용자 입력과 AI 응답을 순서대로 저장합니다.
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=output_text))