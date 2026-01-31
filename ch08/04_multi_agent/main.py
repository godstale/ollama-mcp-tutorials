import os
import uuid
from typing import Annotated

from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from langchain_ollama import ChatOllama
from langchain.agents import create_agent

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()


# 1. 에이전트의 상태를 정의합니다.
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str  # 다음에 실행할 에이전트를 지정합니다.


# 2. 도구를 정의합니다.
# 2-1. 웹 검색 도구
search_tool = TavilySearch(max_results=2)


# 2-2. 파일 저장 도구
@tool
def save_file(filename: str, content: str) -> str:
    """주어진 내용을 지정된 파일명으로 현재 폴더에 저장합니다."""
    with open(filename, "w", encoding="utf-8") as f:
        # 파일 저장 위치를 출력
        print(f"파일이 저장된 위치: {os.path.abspath(filename)}")
        f.write(content)
    return f"'{filename}' 파일이 성공적으로 저장되었습니다."


# 3. 모델과 에이전트를 생성합니다.
llm = ChatOllama(model="qwen3:8b")

# 검색 에이전트는 검색 도구를 사용하도록 설정합니다.
search_agent_executor = create_agent(
    llm,
    [search_tool]
)

# 편집 에이전트는 파일 저장 도구를 사용하도록 설정합니다.
editor_agent_executor = create_agent(
    llm,
    [save_file]
)

# 에이전트 실행 함수를 정의합니다.
def search_agent_node(state: AgentState):
    """검색 에이전트 노드: 웹 검색을 수행합니다."""
    # 시스템 메시지를 추가하여 에이전트의 역할을 지정합니다.
    system_message = SystemMessage(content="당신은 웹 검색을 수행하는 AI입니다. 사용자의 요청에 따라 검색을 수행하고 결과를 정리해서 알려주세요.")
    messages = [system_message] + state["messages"]
    result = search_agent_executor.invoke({"messages": messages})
    return {"messages": result["messages"]}


def editor_agent_node(state: AgentState):
    """편집 에이전트 노드: 파일을 저장합니다."""
    # 시스템 메시지를 추가하여 에이전트의 역할을 지정합니다.
    system_message = SystemMessage(content="당신은 파일을 저장하는 AI입니다. 사용자가 제공한 내용을 적절한 파일명으로 저장하세요.")
    messages = [system_message] + state["messages"]
    result = editor_agent_executor.invoke({"messages": messages})
    return {"messages": result["messages"]}


# 4. 슈퍼바이저를 정의합니다.
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
    """Supervisor 노드: 사용자 요청을 분석하고 적절한 에이전트를 선택합니다."""
    messages = [SystemMessage(content=supervisor_system_message)] + state["messages"]
    response = llm.invoke(messages)

    # 응답에서 다음에 실행할 에이전트를 추출합니다.
    next_agent = "END"
    if "NEXT_AGENT:" in response.content:
        try:
            next_agent = response.content.split("NEXT_AGENT:")[-1].strip()
            if next_agent not in ["Search", "Editor", "END"]:
                next_agent = "END"
        except Exception:
            next_agent = "END"

    return {"messages": [response], "next_agent": next_agent}


# 5. 그래프를 구성합니다.
memory = MemorySaver()
graph_builder = StateGraph(AgentState)


def route_agent(state: AgentState) -> str:
    """다음에 실행할 에이전트를 결정하는 라우터 함수입니다."""
    return state.get("next_agent", "END")


graph_builder.add_node("Supervisor", supervisor)
graph_builder.add_node("Search", search_agent_node)
graph_builder.add_node("Editor", editor_agent_node)

graph_builder.add_edge(START, "Supervisor")
graph_builder.add_conditional_edges(
    "Supervisor", route_agent, {"Search": "Search", "Editor": "Editor", "END": END}
)
graph_builder.add_edge("Search", "Supervisor")
graph_builder.add_edge("Editor", "Supervisor")

# 6. 그래프를 컴파일합니다.
graph = graph_builder.compile(checkpointer=memory)

# 7. 그래프를 시각화합니다.
try:
    png_data = graph.get_graph(xray=True).draw_mermaid_png()
    file_path = os.path.join(os.getcwd(), "graph.png")
    with open(file_path, "wb") as f:
        f.write(png_data)
    print(f"그래프가 {file_path}에 저장되었습니다.")
except Exception as e:
    print(f"그래프 저장 중 오류 발생: {e}")

# 8. 챗봇을 실행합니다.
thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": thread_id}}

while True:
    try:
        user_input = input("질문: ")
        if user_input.lower() == "exit":
            break

        events = graph.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
            stream_mode="values",
        )
        for event in events:
            last_message = event["messages"][-1]
            if hasattr(last_message, "name") and last_message.name == "Supervisor":
                print(f"\nSupervisor: {last_message.content}")
            else:
                print(f"\nAgent: {last_message.content}")

    except Exception as e:
        print(f"챗봇 실행 중 오류 발생: {e}")
        break
