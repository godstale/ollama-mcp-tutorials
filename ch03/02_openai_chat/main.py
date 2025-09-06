from langchain_core.messages import HumanMessage 
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# 1. .env 파일 로드 (API 키) 
load_dotenv() 

# 2. LLM 모델 객체 생성 
llm = ChatOpenAI(model_name="gpt-4.1-mini") 

# 3. 사용자 입력을 받아 모델에 직접 전달
while True:
    user_input = input("질문을 입력하세요 (종료: exit): ")
    if user_input.lower() == "exit":
        break

    # 4. 사용자 입력을 메시지로 포장
    messages = [HumanMessage(content=user_input)]

    # 5. LLM 응답 받기
    response = llm.invoke(messages)

    # 6. 응답 출력
    print("답변:", response.content)
