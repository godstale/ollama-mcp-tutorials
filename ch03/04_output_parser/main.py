from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import JsonOutputParser
import re

# 1. LLM 모델 객체 생성
llm = ChatOllama(model="qwen3:8b")

# 2. 모델 출력 형식 지정
class JsonResponse(BaseModel):
    name: str = Field(description="name of thing")
    date: str = Field(description="date of thing's creation")

# 3. JsonOutputParser 생성
parser = JsonOutputParser(pydantic_object=JsonResponse)

# 4. 사용자 입력을 받아 모델에 직접 전달
while True:
    user_input = input("질문을 입력하세요 (종료: exit): ")
    if user_input.lower() == "exit":
        break

    # 5. 프롬프트 생성
    formatted_prompt = "아래 질문에 대해 name(모델 이름)과 date(만들어진 시기)를 반드시 JSON 형식으로 답변하세요."
    formatted_prompt += f" 질문: {user_input} \n "
    formatted_prompt += f"{parser.get_format_instructions()}"
    messages = [HumanMessage(content=formatted_prompt)]

    # 6. LLM 응답 받기
    response = llm.invoke(messages)

    # 7. JSON 부분만 추출해서 화면에 출력
    json_match = re.search(r'\{[\s\S]*?\}', response.content)
    if json_match:
        json_str = json_match.group(0)
        print(json_str)
    else:
        print("JSON 형식의 답변을 찾지 못했습니다.")
        print("원본 답변:", response.content)
