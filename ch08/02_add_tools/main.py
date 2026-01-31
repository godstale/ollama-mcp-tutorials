import os
from typing import Annotated

from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from langchain.messages import ToolMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict
from langchain_ollama import ChatOllama

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()


# 1. 상태 클래스를 정의합니다.
class State(TypedDict):
    messages: Annotated[list, add_messages]


# 2. 도구를 초기화합니다.
# TavilySearch를 직접 도구 목록에 추가합니다.
tools = [TavilySearch(max_results=2)]
# ToolNode를 사용하여 도구 실행 노드를 생성합니다.
tool_node = ToolNode(tools)

# 3. 모델을 초기화하고 도구를 바인딩합니다.
llm = ChatOllama(model="qwen3:8b")
llm_with_tools = llm.bind_tools(tools)

# 4. 그래프 빌더를 생성합니다.
graph_builder = StateGraph(State)


# 5. 그래프 노드를 정의합니다.
# 5-1. 챗봇 노드: 모델을 호출하여 응답을 생성합니다.
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# 5-2. 도구 라우팅 로직: 모델의 응답에 tool_calls가 있는지 확인합니다.
def route_tools(state: State):
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")

    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END


# 6. 그래프를 구성합니다.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tools": "tools", END: END},
)
graph_builder.add_edge("tools", "chatbot")

# 7. 그래프를 컴파일합니다.
graph = graph_builder.compile()

# 8. 그래프를 시각화하고 파일로 저장합니다.
try:
    png_data = graph.get_graph(xray=True).draw_mermaid_png()
    file_path = os.path.join(os.getcwd(), "graph.png")
    with open(file_path, "wb") as f:
        f.write(png_data)
    print(f"그래프가 {file_path}에 저장되었습니다.")
except Exception as e:
    print(f"그래프 저장 중 오류 발생: {e}")


# 9. 챗봇을 실행합니다.
while True:
    try:
        user_input = input("질문: ")
        if user_input.lower() == "exit":
            break
        # 스트리밍 방식으로 그래프를 실행하고 결과를 출력합니다.
        for event in graph.stream(
            {"messages": [{"role": "user", "content": user_input}]}
        ):
            for value in event.values():
                print("Assistant:", value["messages"][-1].content)
    except Exception as e:
        print(f"챗봇 실행 중 오류 발생: {e}")
        break
