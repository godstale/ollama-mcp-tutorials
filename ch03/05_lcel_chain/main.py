from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# 1. 프롬프트 템플릿 생성
prompt = ChatPromptTemplate.from_messages([
    ("human", "{question}")
])

# 2. LLM 모델 객체 생성
llm = ChatOllama(model="qwen3:8b")

# 3. 모델 출력 형식 지정
output_parser = StrOutputParser()

# 4. LCEL 체인 구성
chain = prompt | llm | output_parser

# 5. 사용자 입력을 받아 체인 실행
while True:
    user_input = input("질문을 입력하세요 (종료: exit): ")
    if user_input.lower() == "exit":
        break

    # 6. 체인 실행 및 결과 처리
    response = chain.invoke(user_input)

    # 7. JSON 부분만 추출해서 화면에 출력
    print(response)
