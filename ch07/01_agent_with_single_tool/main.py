# 1. 필수 라이브러리 임포트
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.messages import HumanMessage, AIMessage

# 2. 환경변수 파일(.env)에서 API 키 등의 설정을 로드
load_dotenv()

# 3. AI 에이전트의 프롬프트 템플릿 정의
prompt = ChatPromptTemplate.from_template(
    """당신은 유능한 기상학자입니다. 필요한 경우 다음 도구들을 사용할 수 있습니다: 
    {tools}

    Important: You must strictly follow the format below. The Final Answer should only appear after a Thought. If no Action is needed, do not skip it or write that you're proceeding without an action — always adhere to the structure.

    Use the following format:
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question
    
    Chat history: {chat_history}
    Question: {question}
    Thought: {agent_scratchpad}
    """
)

# 4. OpenAI의 GPT 모델 초기화
llm = ChatOpenAI(
    temperature=0,
    max_tokens=2048,
    model_name="gpt-4.1-mini"
)

# 5. 검색 도구 설정 (DuckDuckGo 검색 엔진 사용)
tools = [DuckDuckGoSearchRun()]

# 6. ReAct 에이전트 생성 및 실행기 설정
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)
# 7. 대화 기록을 저장할 리스트 초기화
chat_history = []

# 8. 챗봇 시작 메시지 출력
print("기상학자 AI와 대화를 시작합니다. 종료하려면 'q'를 입력하세요.")

# 9. 메인 대화 루프
while True:
    # 10. 사용자 입력 받기
    user_input = input("질문을 입력하세요 (종료: exit): ")
    if user_input.lower() == "exit":
        break

    # 11. 종료 조건 확인
    if user_input.lower() in ("q", "quit", "exit", "종료", "끝"):
        print("대화를 종료합니다.")
        break
        
    # 12. 빈 입력 처리
    if not user_input:
        continue
        
    try:
        # 13. 에이전트 실행 및 응답 생성
        result = agent_executor.invoke({
            "question": user_input, 
            "chat_history": chat_history
        })
        
        # 14. 응답 출력
        response = result["output"]
        print(f"\nAI: {response}")
        
        # 15. 대화 기록에 현재 대화 추가
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response))

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")