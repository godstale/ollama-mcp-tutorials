from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, AIMessageChunk
from langchain_ollama import ChatOllama
from typing import Iterable
from langchain_core.runnables import RunnableGenerator

# 1. 메시지 객체 기반 프롬프트 템플릿 구성
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="당신은 유능한 기상학자입니다. 답변은 200자 이내로 해주세요."),
        MessagesPlaceholder(variable_name="chat_history")
    ]
)

# 2. LLM 모델 설정
llm = ChatOllama(model="qwen3:8b")

# 3. 출력 파서 설정
def replace_word_with_emoji(text: str) -> str:
    return text.replace("태풍", "🌪️ ")

def streaming_parse(chunks: Iterable[AIMessageChunk]) -> Iterable[str]:
    buffer = ""
    for text_chunk in chunks:           # LLM으로부터 받은 각 청크를 처리
        buffer += text_chunk.content    # 현재 버퍼에 새로운 청크의 내용을 추가
        while " " in buffer:            # 버퍼에 공백이 발견되면
            word, buffer = buffer.split(" ", 1)         # 공백 기준 첫 단어와 나머지를 분리
            yield replace_word_with_emoji(word) + " "   # 첫 단어를 처리하고 리턴
    if buffer:
        yield replace_word_with_emoji(buffer)

streaming_parser = RunnableGenerator(streaming_parse)

# 4. 체인 구성
chain = prompt | llm | streaming_parser

# 5. 채팅 기록 저장용 배열
chat_history = []

# 6. 사용자 입력을 받아 체인 실행
while True:
    user_input = input("질문을 입력하세요 (종료: exit): ")
    if user_input.lower() == "exit":
        break

    result = ""
    chat_history.append(HumanMessage(content=user_input))
    for chunk in chain.stream({"chat_history": chat_history}):
        print(chunk, end="", flush=True)
        result += chunk
    chat_history.append(AIMessage(content=result))
    print("\n")
