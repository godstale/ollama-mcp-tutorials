import os
import uuid
import re
from typing import Annotated

from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
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
    [search_tool],
    system_prompt="당신은 웹 검색을 수행하는 AI입니다. 사용자의 요청에 따라 검색을 수행하고 결과를 정리해서 알려주세요."
)

# 편집 에이전트는 파일 저장 도구를 사용하도록 설정합니다.
editor_agent_executor = create_agent(
    llm,
    [save_file],
    system_prompt="당신은 파일을 저장하는 AI입니다. 사용자가 제공한 내용을 적절한 파일명으로 저장하세요. 반드시 save_file 도구를 사용하여 파일을 저장하고, 도구가 반환한 저장 위치를 사용자에게 알려주세요."
)

# 에이전트 실행 함수를 정의합니다.
def search_agent_node(state: AgentState):
    """검색 에이전트 노드: 웹 검색을 수행합니다."""
    print("\n[DEBUG] Search 에이전트 노드 실행 중...")
    print(f"[DEBUG] 입력 메시지 수: {len(state['messages'])}")
    # create_agent의 system_prompt가 자동으로 시스템 메시지를 추가합니다.
    result = search_agent_executor.invoke({"messages": state["messages"]})
    print(f"[DEBUG] Search 에이전트 응답 메시지 수: {len(result['messages'])}")
    return {"messages": result["messages"]}


def editor_agent_node(state: AgentState):
    """편집 에이전트 노드: 파일을 저장합니다."""
    print("\n[DEBUG] Editor 에이전트 노드 실행 중...")
    print(f"[DEBUG] 입력 메시지 수: {len(state['messages'])}")

    # create_agent의 system_prompt가 자동으로 시스템 메시지를 추가합니다.
    result = editor_agent_executor.invoke({"messages": state["messages"]})

    print(f"[DEBUG] Editor 에이전트 응답 메시지 수: {len(result['messages'])}")

    # 도구 호출 여부 확인
    for msg in result["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            print(f"[DEBUG] 도구 호출 발견: {msg.tool_calls}")
        if hasattr(msg, "name"):
            print(f"[DEBUG] 도구 응답 발견: name={msg.name}")

    return {"messages": result["messages"]}


# 4. 슈퍼바이저를 정의합니다.
supervisor_system_message = """당신은 작업을 관리하는 Supervisor입니다.
사용자의 요청을 분석하고 적절한 에이전트를 선택해야 합니다.

사용 가능한 에이전트:
1. Search: 웹 검색이 필요한 질문이나 최신 정보가 필요한 경우
2. Editor: 파일 저장이나 편집이 필요한 경우

**중요**: 대화 히스토리를 반드시 확인하여 다음 조건을 체크하세요:
- Search 에이전트가 이미 검색을 완료했는지
- Editor 에이전트가 이미 파일을 저장했는지 (도구 save_file이 호출되었는지)
- 사용자의 모든 요청이 처리되었는지

다음 중 하나를 선택하세요:
- 아직 검색이 필요하고 검색하지 않은 경우: "Search"
- 파일 저장이 필요하고 아직 저장하지 않은 경우: "Editor"
- **모든 작업이 완료된 경우 (검색 완료, 파일 저장 완료 등): 반드시 "END"**

응답 형식:
1. 대화 히스토리 분석 (어떤 작업이 완료되었는지)
2. 다음에 필요한 작업 또는 작업 완료 여부
3. 마지막에 반드시 "NEXT_AGENT: [선택한_에이전트]" 형태로 명시
"""


def supervisor(state: AgentState):
    """Supervisor 노드: 사용자 요청을 분석하고 적절한 에이전트를 선택합니다."""
    print("\n[DEBUG] Supervisor 노드 실행 중...")
    print(f"[DEBUG] 현재 메시지 수: {len(state['messages'])}")

    # 무한 루프 방지: 메시지가 너무 많으면 강제 종료
    if len(state["messages"]) > 20:
        print("[WARNING] 메시지 수가 20개를 초과하여 강제 종료합니다.")
        return {
            "messages": [
                AIMessage(content="작업을 완료했습니다. 더 이상 진행하지 않습니다.")
            ],
            "next_agent": "END",
        }

    messages = [SystemMessage(content=supervisor_system_message)] + state["messages"]
    response = llm.invoke(messages)

    # 응답에서 다음에 실행할 에이전트를 추출합니다.
    next_agent = "END"
    if "NEXT_AGENT:" in response.content:
        try:
            next_agent = response.content.split("NEXT_AGENT:")[-1].strip()
            print(f"[DEBUG] Supervisor가 선택한 다음 에이전트: {next_agent}")
            if next_agent not in ["Search", "Editor", "END"]:
                print(f"[WARNING] 유효하지 않은 에이전트: {next_agent}, END로 변경")
                next_agent = "END"
        except Exception as e:
            print(f"[ERROR] 에이전트 추출 중 오류: {e}")
            next_agent = "END"
    else:
        print("[DEBUG] NEXT_AGENT가 응답에 없음, END로 설정")

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

        print(f"\n[DEBUG] 사용자 입력: {user_input}")
        events = graph.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
            stream_mode="values",
        )
        for event in events:
            print(f"[DEBUG] 이벤트 수신, 메시지 수: {len(event.get('messages', []))}")
            last_message = event["messages"][-1]

            # 메시지 타입 확인
            msg_type = type(last_message).__name__
            print(f"[DEBUG] 메시지 타입: {msg_type}")

            if hasattr(last_message, "name") and last_message.name == "Supervisor":
                print(f"\nSupervisor: {last_message.content}")
            else:
                print(f"\nAgent: {last_message.content}")

    except Exception as e:
        print(f"챗봇 실행 중 오류 발생: {e}")
        break
