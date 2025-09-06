import json
import os
from typing import Annotated

from dotenv import load_dotenv
from langchain.agents import Tool
from langchain.chat_models import init_chat_model
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain_core.messages import ToolMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

# 환경 변수 로드 (.env 파일에서 API 키 등을 로드)
load_dotenv()


# 1. 상태 클래스 정의
class State(TypedDict):
    messages: Annotated[list, add_messages]


# 2. 도구 추가
search_tool = Tool(
    name="WebSearch",
    func=TavilySearchResults().run,
    description="This is a real-time web search tool (based on Tavily service)",
)
tools = [search_tool]

# 3. 모델 초기화
llm = init_chat_model("openai:gpt-4.1-mini")
llm_with_tools = llm.bind_tools(tools)

# 4. 그래프 빌더 생성
graph_builder = StateGraph(State)


# 5. 노드 정의
# 5-1. 챗봇 노드 정의 (모델 호출)
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# 5-2. 도구 노드 정의
class BasicToolNode:
    """도구 호출을 처리하는 노드"""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}


tool_node = BasicToolNode(tools=tools)


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


# 7. 그래프 생성
# 7-1. 그래프 노드 추가
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

# 7-2. 그래프 엣지 추가
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    # route_tools 함수의 출력에 따라 다음 노드 결정
    {"tools": "tools", END: END},
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)

# 7-3. 그래프 컴파일
graph = graph_builder.compile()

# 8. 그래프 시각화
try:
    # 8-1. 그래프를 PNG 파일로 저장
    png_data = graph.get_graph(xray=True).draw_mermaid_png()
    # 8-2. 현재 작업 디렉토리에 'graph.png' 파일로 저장
    file_path = os.path.join(os.getcwd(), "graph.png")
    with open(file_path, "wb") as f:
        f.write(png_data)
    print(f"Graph saved as {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")


# 9. 챗봇 실행
while True:
    try:
        # 9-1. 사용자 입력 받기
        user_input = input("질문을 입력하세요 (종료: exit): ")
        if user_input.lower() == "exit":
            break
        # 8-2. 그래프 실행 및 결과 출력
        for event in graph.stream(
            {"messages": [{"role": "user", "content": user_input}]}
        ):
            for value in event.values():
                print("Assistant:", value["messages"][-1].content)
    except Exception as e:
        print(f"Error while running the chatbot: {e}")
        break
