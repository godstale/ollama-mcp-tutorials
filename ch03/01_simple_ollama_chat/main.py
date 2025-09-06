from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# 1. LLM 모델 객체 생성
llm = ChatOllama(model="qwen3:8b")

# 2. 사용자 입력을 받아 모델에 직접 전달
while True:
    user_input = input("질문을 입력하세요 (종료: exit): ")
    if user_input.lower() == "exit":
        break

    # 3. 사용자 입력을 메시지로 포장
    messages = [HumanMessage(content=user_input)]

    # 4. LLM 응답 받기
    response = llm.invoke(messages)

    # 5. 응답 출력
    print("답변:", response.content)
