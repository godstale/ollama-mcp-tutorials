import asyncio
import os
import sys
import uuid
from typing import Annotated, Any, List, Optional

import nest_asyncio
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from mcp_manager import cleanup_mcp_client, initialize_mcp_client
from mcp_prompt import MCP_CHAT_PROMPT, SUPERVISOR_PROMPT
from typing_extensions import TypedDict

# 환경 변수 로드 (.env 파일에서 API 키 등을 로드)
load_dotenv()

DEFAULT_TEMPERATURE = 0.3
MODEL_GPT = "gpt-4o-mini"
NODE_SUPERVISOR = "Supervisor"
NODE_COMMON = "Common"


# 1. 상태 클래스 정의
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str  # 다음 실행할 에이전트 정보


# 2. 모델 초기화, 검색 및 편집 에이전트 생성
# 2-1. 채팅 모델 생성: 도구 사용이 가능한 LLM 모델 필요
chat_model = ChatOpenAI(
    model=MODEL_GPT,
    temperature=DEFAULT_TEMPERATURE,
)


# 2-2. 에이전트 생성
def create_common_agent(mcp_tools: Optional[List] = None):
    # ReAct 에이전트 생성 (langchain.agents.create_agent 사용)
    common_agent = create_agent(
        model=chat_model, tools=mcp_tools, system_prompt=MCP_CHAT_PROMPT
    )
    print("Common agent created.")
    return common_agent  # 에이전트 반환


# 3. Supervisor 노드 정의
async def supervisor(state: AgentState):
    """Supervisor 노드: 사용자 요청을 분석하고 적절한 에이전트를 선택"""
    print("\n[Supervisor] ===== 사용자 요청 분석 시작 =====")
    print(f"[Supervisor] 메시지 개수: {len(state['messages'])}")

    # 마지막 사용자 메시지 출력
    user_messages = [msg for msg in state["messages"] if hasattr(msg, 'type') and msg.type == 'human']
    if user_messages:
        print(f"[Supervisor] 사용자 요청: {user_messages[-1].content}")

    messages = [SystemMessage(content=SUPERVISOR_PROMPT)] + state["messages"]
    print("[Supervisor] LLM 모델 호출 중...")
    response = await chat_model.ainvoke(messages)
    print("\n[Supervisor] ===== LLM 분석 결과 =====")
    print(response.content)
    print("[Supervisor] ===== 분석 완료 =====\n")

    # 응답에서 다음 에이전트 추출
    next_agent = "END"  # 기본값
    if "NEXT_AGENT:" in response.content:
        try:
            next_agent = response.content.split("NEXT_AGENT:")[-1].strip()
            if next_agent not in [NODE_COMMON, "END"]:
                print(f"[Supervisor] ⚠️ 경고: 알 수 없는 에이전트 '{next_agent}', 'END'로 변경")
                next_agent = "END"
            print(f"[Supervisor] ✅ 다음 에이전트 결정: {next_agent}")
        except Exception as e:
            print(f"[Supervisor] ❌ 에이전트 추출 실패: {e}, 기본값 'END' 사용")
            next_agent = "END"
    else:
        print(f"[Supervisor] ⚠️ NEXT_AGENT 키워드 없음, 기본값 'END' 사용")

    return {"messages": [response], "next_agent": next_agent}


# 4. 라우터 함수 정의 (에이전트 선택)
def route_agent(state: AgentState) -> str:
    next_agent = state.get("next_agent", "END")
    print(f"\n[Router] 🔀 라우팅: {next_agent}")
    if next_agent == NODE_COMMON:
        print("[Router] → Common 에이전트로 이동 (MCP 도구 사용 가능)")
    elif next_agent == "END":
        print("[Router] → 작업 종료")
    return next_agent


# 5. 그래프 빌드
def build_graph(common_mcp_tools):
    # 에이전트 생성 및 초기화
    common_agent = create_common_agent(mcp_tools=common_mcp_tools)

    # 메모리 초기화
    memory = MemorySaver()

    # 그래프 빌더 생성
    graph_builder = StateGraph(AgentState)

    # 노드 추가
    graph_builder.add_node(NODE_SUPERVISOR, supervisor)
    graph_builder.add_node(NODE_COMMON, common_agent)

    # 엣지 추가
    graph_builder.add_edge(START, NODE_SUPERVISOR)
    graph_builder.add_conditional_edges(
        NODE_SUPERVISOR, route_agent, {NODE_COMMON: NODE_COMMON, "END": END}
    )
    graph_builder.add_edge(NODE_COMMON, END)

    # 그래프 컴파일
    graph = graph_builder.compile(checkpointer=memory)

    # 그래프 시각화
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

    return graph


# 6. 메인 함수
async def async_main():
    # 대화 스레드 ID 설정: 이 ID를 기준으로 메모리가 저장되고 로드
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    # Initialize MCP client
    mcp_client = None
    try:
        print("\n=== Initializing MCP client... ===")
        mcp_client, mcp_tools = await initialize_mcp_client()
        print(f"Loaded {len(mcp_tools)} MCP tools.")

        # Print MCP tool information
        for tool in mcp_tools:
            print(f"[Tool] {tool.name}")

        # 에이전트 생성 및 그래프 빌드
        graph = build_graph(mcp_tools)

        while True:
            # 사용자 입력 받기
            user_input = input("질문을 입력하세요 (종료: exit): ")
            if user_input.lower() == "exit":
                break

            # 그래프 비동기 스트리밍 실행
            try:
                print("\n" + "="*60)
                print("그래프 실행 시작")
                print("="*60)
                async for event in graph.astream(
                    {
                        "messages": [
                            ("system", SUPERVISOR_PROMPT),  # Supervisor 프롬프트는 여기에
                            ("user", user_input),
                        ]
                    },
                    config=config,
                    stream_mode="values",
                ):
                    # 각 노드의 실행 결과를 실시간으로 출력
                    if "messages" in event and event["messages"]:
                        last_message = event["messages"][-1]

                        # 노드 이름에 따라 다른 출력 형식 사용
                        if hasattr(last_message, "name"):
                            if last_message.name == NODE_SUPERVISOR:
                                print("\n[Supervisor 응답]")
                                print(last_message.content)
                            elif last_message.name == NODE_COMMON:
                                print("\n[Common Agent 응답]")
                                print(last_message.content)
                            else:
                                print(f"\n[{last_message.name} 응답]")
                                print(last_message.content)
                        else:
                            # 도구 호출 결과나 일반 메시지
                            if (
                                hasattr(last_message, "tool_calls")
                                and last_message.tool_calls
                            ):
                                print("\n[도구 호출 중]")
                                for tool_call in last_message.tool_calls:
                                    print(f"  - 도구: {tool_call.get('name', 'unknown')}")
                                    print(f"  - 입력: {tool_call.get('args', {})}")
                            elif hasattr(last_message, "content") and last_message.content:
                                # 도구 실행 결과
                                if hasattr(last_message, "name"):
                                    print(f"\n[도구 실행 결과: {last_message.name}]")
                                    print(last_message.content)
                                else:
                                    print("\n[메시지]")
                                    print(last_message.content)

                    # next_agent 정보가 있으면 출력
                    if "next_agent" in event:
                        print(f"\n[라우팅] 다음 에이전트: {event['next_agent']}")

                print("\n" + "="*60)
                print("그래프 실행 완료")
                print("="*60)

            except Exception as e:
                print(f"\nError during graph execution: {str(e)}")
                import traceback

                print(traceback.format_exc())

    except Exception as e:
        print(f"\n\nAn critical error occurred during setup or execution: {str(e)}")
        import traceback

        print(traceback.format_exc())
    finally:
        # Clean up MCP client (remains the same)
        if mcp_client is not None:
            print("\nCleaning up MCP client...")
            await cleanup_mcp_client(mcp_client)
            print("MCP client cleanup complete.")


try:
    nest_asyncio.apply()
    asyncio.run(async_main())
except SystemExit:
    # Raised by sys.exit(), like in handle_sigint or API key check
    print("Exiting program.")
except Exception as e:
    print(f"\n\nAn error occurred during program execution: {str(e)}")
    import traceback

    print(traceback.format_exc())
    sys.exit(1)  # Exit with error code
