import asyncio
import os
import sys
import uuid
from typing import Annotated, Any, List, Optional

import nest_asyncio
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.graph import CompiledGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import create_react_agent
from mcp_manager import cleanup_mcp_client, initialize_mcp_client
from mcp_prompt import MCP_CHAT_PROMPT, SUPERVISOR_PROMPT
from typing_extensions import TypedDict

# 환경 변수 로드 (.env 파일에서 API 키 등을 로드)
load_dotenv()

DEFAULT_TEMPERATURE = 0.3
MODEL_QWEN3 = "qwen3:8b"
MODEL_OPENAI = "gpt-4.1-mini"
NODE_SUPERVISOR = "Supervisor"
NODE_COMMON = "Common"


# 1. 상태 클래스 정의
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str  # 다음 실행할 에이전트 정보


# 2. 모델 초기화, 검색 및 편집 에이전트 생성
# 2-1. 채팅 모델 생성: 도구 사용이 가능한 LLM 모델 필요
# chat_model = ChatOllama(
#     model=MODEL_QWEN3,
#     temperature=DEFAULT_TEMPERATURE,
# )
chat_model = ChatOpenAI(model_name=MODEL_OPENAI, temperature=DEFAULT_TEMPERATURE)


# 2-2. 에이전트 생성
def create_agent(mcp_tools: Optional[List] = None) -> CompiledGraph:
    # ReAct 에이전트 생성
    react_agent = create_react_agent(model=chat_model, tools=mcp_tools)
    print("ReAct agent created.")
    return react_agent  # 에이전트 반환


# 3. Supervisor 노드 정의
async def supervisor(state: AgentState):
    """Supervisor 노드: 사용자 요청을 분석하고 적절한 에이전트를 선택"""
    print(f"\n[Supervisor] 사용자 요청 분석 시작: {len(state['messages'])}개 메시지")

    messages = [SystemMessage(content=SUPERVISOR_PROMPT)] + state["messages"]
    print("[Supervisor] LLM 모델 호출 중...")
    response = await chat_model.ainvoke(messages)
    print(f"[Supervisor] LLM 응답: {response.content}")

    # 응답에서 다음 에이전트 추출
    next_agent = "END"  # 기본값
    if "NEXT_AGENT:" in response.content:
        try:
            next_agent = response.content.split("NEXT_AGENT:")[-1].strip()
            if next_agent not in [NODE_COMMON, "END"]:
                next_agent = "END"
            print(f"[Supervisor] 다음 에이전트 결정: {next_agent}")
        except:
            next_agent = "END"
            print(f"[Supervisor] 에이전트 추출 실패, 기본값 사용: {next_agent}")
    else:
        print(f"[Supervisor] NEXT_AGENT 키워드 없음, 기본값 사용: {next_agent}")

    return {"messages": [response], "next_agent": next_agent}


# 4. 라우터 함수 정의 (에이전트 선택)
def route_agent(state: AgentState) -> str:
    return state.get("next_agent", "END")


# 5. 그래프 빌드
def build_graph(common_mcp_tools):
    # 에이전트 생성 및 초기화
    common_agent = create_agent(mcp_tools=common_mcp_tools)

    # 메모리 초기화
    # memory = MemorySaver()

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
    graph = graph_builder.compile()
    # graph = graph_builder.compile(checkpointer=memory)

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

        # 도구 정보를 포맷팅하여 시스템 프롬프트 생성
        tool_names = [tool.name for tool in mcp_tools] if mcp_tools else []
        tools_description = (
            "\n".join([f"- {tool.name}: {tool.description}" for tool in mcp_tools])
            if mcp_tools
            else "No tools available"
        )
        formatted_mcp_prompt = MCP_CHAT_PROMPT.format(
            tools=tools_description, tool_names=", ".join(tool_names)
        )

        while True:
            # 사용자 입력 받기
            user_input = "긱뉴스에서 오늘 인공지능 관련 뉴스 중요도 순으로 5개 찾아서 나열해줘. 5개 뉴스는 링크뿐만 아니라 요약한 내용을 같이 표시해줘. 그리고 노션에 새 페이지 생성해서 답변 결과을 입력해줘. 새 페이지 제목과 내용을 블로그 포스트처럼 친근하게 작성해줘. 새 페이지 추가할 노션 데이터베이트 ID : 24acafed095681a8be96c93fc6dede04"
            if user_input.lower() == "exit":
                break

            # 그래프 비동기 스트리밍 실행
            try:
                print("\n=== 그래프 실행 시작 ===")
                async for event in graph.astream(
                    {
                        "messages": [
                            ("system", formatted_mcp_prompt),
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
                                print(f"\n[Supervisor] {last_message.content}")
                            elif last_message.name == NODE_COMMON:
                                print(f"\n[Common Agent] {last_message.content}")
                            else:
                                print(f"\n[{last_message.name}] {last_message.content}")
                        else:
                            # 도구 호출 결과나 일반 메시지
                            if (
                                hasattr(last_message, "tool_calls")
                                and last_message.tool_calls
                            ):
                                print(f"\n[Tool Call] {last_message.content}")
                            else:
                                print(f"\n[Message] {last_message.content}")

                    # next_agent 정보가 있으면 출력
                    if "next_agent" in event:
                        print(f"\n[Routing] 다음 에이전트: {event['next_agent']}")

                print("\n=== 그래프 실행 완료 ===")
            
                # 1분 딜레이 추가
                print("\n1분 대기 중...")
                await asyncio.sleep(60)
                print("대기 완료. 다음 실행을 위해 준비됩니다.")

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
