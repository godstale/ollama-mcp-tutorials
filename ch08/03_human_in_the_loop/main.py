import json
import os
from typing import Annotated

from dotenv import load_dotenv
from langchain.agents import Tool
from langchain.chat_models import init_chat_model
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command, interrupt
from typing_extensions import TypedDict

# 환경 변수 로드 (.env 파일에서 API 키 등을 로드)
load_dotenv()


# 1. 상태 클래스 정의
class State(TypedDict):
    messages: Annotated[list, add_messages]


# 2. 도구 추가
# 2-1. 웹 검색 도구
search_tool = Tool(
    name="WebSearch",
    func=TavilySearchResults().run,
    description="This is a real-time web search tool (based on Tavily service)",
)


# 2-2. 사용자 입력 도구
@tool
def human_assistance(query: str) -> str:
    """사용자의 입력이 필요한 경우 이 도구를 호출하여 도움을 요청합니다."""
    human_response = interrupt({"query": query})
    return human_response["data"]


tools = [search_tool, human_assistance]

# 3. 모델 초기화
llm = init_chat_model("openai:gpt-4.1-mini")
llm_with_tools = llm.bind_tools(tools)

# 4. 그래프 빌더 생성
graph_builder = StateGraph(State)


# 5. 노드 정의
# 5-1. 챗봇 노드 정의 (모델 호출)
def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    return {"messages": [message]}


tool_node = ToolNode(tools=tools)


# 6. 도구 노드 라우팅
def route_tools(
    state: State,
):
    """
    메시지에 tool_calls가 있으면 "tools"로 라우팅, 없으면 END로 라우팅
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    # 도구 호출인 경우 "tools"를 리턴, 아니면 END를 리턴
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END


# 6. 그래프 생성
# 6-1. 그래프 노드 추가
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

# 6-2. 그래프 엣지 추가
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    # route_tools 함수의 출력에 따라 다음 노드 결정
    {"tools": "tools", END: END},
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)

# 6-3. 메모리 초기화
memory = MemorySaver()

# 6-4. 그래프 컴파일
graph = graph_builder.compile(checkpointer=memory)

# 7. 그래프 시각화
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


# 8. 챗봇 실행
while True:
    try:
        # 8-1. 사용자 입력 받기
        user_input = input("질문을 입력하세요 (종료: exit): ")
        if user_input.lower() == "exit":
            break
        # 8-2. 그래프 실행 및 결과 출력
        config = {"configurable": {"thread_id": "2131231"}}
        # 8-3. 그래프 실행 및 결과 출력
        graph_stream = graph.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
            stream_mode="values",
        )
        for event in graph_stream:
            if "messages" in event:
                last_msg = event["messages"][-1]
                last_msg.pretty_print()

                # human_assistance 도구의 interrupt 신호 감지
                if (
                    hasattr(last_msg, "tool_calls")
                    and isinstance(last_msg.tool_calls, list)
                    and any(
                        tc["name"] == "human_assistance" for tc in last_msg.tool_calls
                    )
                ):
                    # 첫 번째 human_assistance 도구 호출 가져오기
                    tool_call = next(
                        tc
                        for tc in last_msg.tool_calls
                        if tc["name"] == "human_assistance"
                    )
                    tool_call_id = tool_call["id"]

                    # 사용자 입력 요청
                    human_input = input("🧑 입력해주세요: ")

                    # 그래프 resume
                    command = Command(resume={"data": human_input})
                    for event in graph.stream(command, config, stream_mode="values"):
                        if "messages" in event:
                            last_msg = event["messages"][-1]
                            last_msg.pretty_print()

    except Exception as e:
        print(f"Error while running the chatbot: {e}")
        break
