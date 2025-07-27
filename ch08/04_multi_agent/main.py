import os
import uuid
from typing import Annotated

from dotenv import load_dotenv
from langchain.agents import Tool
from langchain.chat_models import init_chat_model
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent
from typing_extensions import TypedDict

# 환경 변수 로드 (.env 파일에서 API 키 등을 로드)
load_dotenv()


# 1. 상태 클래스 정의
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str  # 다음 실행할 에이전트 정보


# 2. 도구 추가
# 2-1. 웹 검색 도구
search_tool = Tool(
    name="WebSearch",
    func=TavilySearchResults().run,
    description="This is a real-time web search tool (based on Tavily service)",
)


# 2-2. 파일 저장 에이전트용 도구
@tool
def save_file(filename: str, content: str) -> str:
    """주어진 내용을 지정된 파일명으로 현재 폴더에 저장합니다."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"'{filename}' 파일이 성공적으로 저장되었습니다."


# 3. 모델 초기화, 검색 및 편집 에이전트 생성
llm = init_chat_model("openai:gpt-4.1-mini")
search_agent = create_react_agent(llm, [search_tool])
editor_agent = create_react_agent(llm, [save_file])


# 4. Supervisor 시스템 메시지 정의
supervisor_system_message = """당신은 작업을 관리하는 Supervisor입니다. 
사용자의 요청을 분석하고 적절한 에이전트를 선택해야 합니다.

사용 가능한 에이전트:
1. Search: 웹 검색이 필요한 질문이나 최신 정보가 필요한 경우
2. Editor: 파일 저장이나 편집이 필요한 경우

사용자의 요청에 따라 다음 중 하나를 선택하세요:
- 검색이 필요한 경우: "Search"
- 파일 저장/편집이 필요한 경우: "Editor"
- 일반 대화나 작업 완료인 경우: "END"

응답 형식:
1. 먼저 사용자 요청을 분석하고 설명
2. 선택한 에이전트와 그 이유를 명시
3. 마지막에 반드시 "NEXT_AGENT: [선택한_에이전트]" 형태로 명시
"""


def supervisor(state: AgentState):
    """Supervisor 노드: 사용자 요청을 분석하고 적절한 에이전트를 선택"""
    messages = [SystemMessage(content=supervisor_system_message)] + state["messages"]
    response = llm.invoke(messages)

    # 응답에서 다음 에이전트 추출
    next_agent = "END"  # 기본값
    if "NEXT_AGENT:" in response.content:
        try:
            next_agent = response.content.split("NEXT_AGENT:")[-1].strip()
            if next_agent not in ["Search", "Editor", "END"]:
                next_agent = "END"
        except:
            next_agent = "END"

    return {"messages": [response], "next_agent": next_agent}


# 4. 메모리 초기화
memory = MemorySaver()

# 5. 그래프 빌더 생성
graph_builder = StateGraph(AgentState)


# 6. 라우터 함수 정의 (에이전트 선택)
def route_agent(state: AgentState) -> str:
    return state.get("next_agent", "END")


# 7. 그래프에 노드 및 엣지 추가가
graph_builder.add_node("Supervisor", supervisor)
graph_builder.add_node("Search", search_agent)
graph_builder.add_node("Editor", editor_agent)

# START에서 Supervisor로 진입
graph_builder.add_edge(START, "Supervisor")
# Supervisor에서 조건부 라우팅
graph_builder.add_conditional_edges(
    "Supervisor", route_agent, {"Search": "Search", "Editor": "Editor", "END": END}
)
# 각 에이전트 실행 후 종료
graph_builder.add_edge("Search", "Supervisor")
graph_builder.add_edge("Editor", "Supervisor")

# 8. 그래프 컴파일
graph = graph_builder.compile(checkpointer=memory)

# 9. 그래프 시각화
try:
    # 그래프를 PNG 파일로 저장
    png_data = graph.get_graph(xray=True).draw_mermaid_png()
    # 현재 작업 디렉토리에 'graph.png' 파일로 저장
    file_path = os.path.join(os.getcwd(), "graph.png")
    with open(file_path, "wb") as f:
        f.write(png_data)
    print(f"Graph saved as {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")

# 대화 스레드 ID 설정: 이 ID를 기준으로 메모리가 저장되고 로드
thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": thread_id}}

# 10. 챗봇 실행
while True:
    try:
        # 10-1. 사용자 입력 받기
        user_input = input("질문을 입력하세요 (종료: exit): ")
        if user_input.lower() == "exit":
            break
        # 10-2. 그래프 실행
        events = graph.stream(
            {"messages": [("user", user_input)]},
            config=config,
            # stream_mode="values"는 각 단계의 최종 상태 객체를 반환
            stream_mode="values",
        )
        # 10-3. 그래프 실행 결과 출력
        for event in events:
            last_message = event["messages"][-1]
            if hasattr(last_message, "name") and last_message.name == "Supervisor":
                print(f"\nSupervisor: {last_message.content}")
            else:
                print(f"\nAgent: {last_message.content}")

    except Exception as e:
        print(f"Error while running the chatbot: {e}")
        break
