from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

# 1. 올라마 임베딩 모델을 사용할 수 있도록 준비
bge_embed = OllamaEmbeddings(model="bge-m3")

# 2. 벡터 스토어 구축
knowledge = [
    "부모님 용돈 : 50만원",
    "학원비 : 40만원",
    "마트 장보기 : 30만원",
    "학교 급식비 : 20만원",
]
print("이번달 가계부", knowledge)

vector_store = FAISS.from_texts(knowledge, embedding=bge_embed)
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# 3. 사용자로부터 질문 입력 받음
qeustion = input(f"질문을 입력하세요: ")

# 4. 사용자 질문과 유사한 벡터 검색
contexts = retriever.invoke(qeustion)
results = "\n".join(context.page_content for context in contexts)
print(f"\nretrieved size: {len(contexts)}")
print(results)
