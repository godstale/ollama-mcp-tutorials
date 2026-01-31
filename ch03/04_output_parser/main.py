from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage

# 1. LLM 모델 객체 생성
# with_structured_output을 사용하여 JSON 출력을 지원하도록 모델을 설정
llm = ChatOllama(model="qwen3:8b", format="json")

# 2. 모델 출력 형식 지정
class JsonResponse(BaseModel):
    name: str = Field(description="name of thing")
    date: str = Field(description="date of thing's creation")

# 3. 구조화된 출력을 사용하도록 LLM 설정
structured_llm = llm.with_structured_output(JsonResponse)

# 4. 사용자 입력을 받아 모델에 직접 전달
while True:
    user_input = input("질문을 입력하세요 (종료: exit): ")
    if user_input.lower() == "exit":
        break

    # 5. 프롬프트 생성 (포맷 지침이 필요 없음)
    prompt = f"아래 질문에 대해 name(모델 이름)과 date(만들어진 시기)를 반드시 JSON 형식으로 답변하세요. 질문: {user_input}"
    messages = [HumanMessage(content=prompt)]

    try:
        # 6. 구조화된 LLM 실행
        response = structured_llm.invoke(messages)

        # 7. 파싱된 JSON 객체를 직접 사용
        print("Name:", response.name)
        print("Date:", response.date)

    except Exception as e:
        print("오류가 발생했습니다:", e)
