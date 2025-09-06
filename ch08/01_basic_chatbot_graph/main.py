import os
from typing import Annotated

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

# 환경 변수 로드 (.env 파일에서 API 키 등을 로드)
load_dotenv()


# 1. 상태 클래스 정의
class State(TypedDict):
    messages: Annotated[list, add_messages]


# 2. 모델 초기화
llm = init_chat_model("ollama:qwen3:8b")

# 3. 그래프 빌더 생성
graph_builder = StateGraph(State)


# 4. 챗봇 노드 정의 (모델 호출)
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


# 5. 그래프 생성
# 5-1. 그래프 노드 추가
graph_builder.add_node("chatbot", chatbot)

# 5-2. 그래프 엣지 추가
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# 5-3. 그래프 컴파일
graph = graph_builder.compile()

# 6. 그래프 시각화
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


# 7. 챗봇 실행
while True:
    try:
        # 7-1. 사용자 입력 받기
        user_input = input("질문을 입력하세요 (종료: exit): ")
        if user_input.lower() == "exit":
            break
        # 7-2. 그래프 실행 및 결과 출력
        for event in graph.stream(
            {"messages": [{"role": "user", "content": user_input}]}
        ):
            for value in event.values():
                print("Assistant:", value["messages"][-1].content)
    except Exception as e:
        print(f"Error while running the chatbot: {e}")
        break
