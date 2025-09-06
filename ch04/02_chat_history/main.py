from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

# 1. 프롬프트 템플릿 정의
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 유능한 기상학자입니다. 답변은 200자 이내로 해주세요."),
        MessagesPlaceholder("chat_history"),
        ("human", "{question}"),
    ]
)

# 2. LLM 모델 설정
llm = ChatOllama(model="qwen3:8b")

# 3. 출력 파서 설정
output_parser = StrOutputParser()

# 4. 프롬프트 → 모델 → 출력 파서 체인 구성
chain = prompt | llm | output_parser

# 5. 채팅 기록 저장용 배열
chat_history = []

# 6. 사용자 입력을 받아 체인 실행
while True:
    user_input = input("질문을 입력하세요 (종료: exit): ")
    if user_input.lower() == "exit":
        break

    result = ""
    for chunk in chain.stream({"question": user_input, "chat_history": chat_history}):
        print(chunk, end="", flush=True)
        result += chunk
    chat_history.append(("human", user_input))
    chat_history.append(("ai", result))
    print("\n")
