import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()  # .env 파일 로드

# 벡터 DB 파일 경로
VECTOR_DB_PATH = "faiss_index"


# 1. 벡터 DB 파일이 없으면 생성 후 vector_store 리턴
def create_vector_db():
    # 1-1. 문서 로딩 (Document Loading)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(current_dir, "news_weather.pdf")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    print(f"문서의 수: {len(docs)}")

    # 1-2. 문서 분할 (Splitting)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=70)
    splits = text_splitter.split_documents(docs)
    print(f"split size: {len(splits)}")

    # 1-3. 임베딩 생성 (Embedding)
    embeddings = OllamaEmbeddings(model="qwen3:8b")

    # 1-4. 벡터 저장소 구축 (Vector Database)
    vector_store = FAISS.from_documents(
        documents=splits,
        embedding=embeddings,
    )

    # 1-5. 벡터 DB를 로컬에 저장
    vector_store.save_local(VECTOR_DB_PATH)

    return vector_store


# 2. 메인 로직
if os.path.exists(VECTOR_DB_PATH):
    print("기존 벡터 DB를 로드합니다.")
    embeddings = OllamaEmbeddings(model="qwen3:8b")
    vector_store = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )
else:
    print("새로운 벡터 DB를 생성합니다.")
    vector_store = create_vector_db()


# 3. 쿼리 저장소 검색을 위한 retriever 생성
retriever = vector_store.as_retriever()

# 4. PROMPT Template 생성
prompt = PromptTemplate.from_template(
    """당신은 질문-답변(Question-Answering)을 수행하는 AI 어시스턴트입니다.
당신의 임무는 주어진 문맥(context) 에서 주어진 질문(question) 에 답하는 것입니다.
검색된 다음 문맥(context)을 사용하여 질문(question) 에 답하세요. 
만약, 주어진 문맥(context) 에서 답을 찾을 수 없다면, 
답을 모른다면 `주어진 정보에서 질문에 대한 정보를 찾을 수 없습니다` 라고 답하세요.
질문과 관련성이 높은 내용만 답변하고 추측된 내용을 생성하지 마세요. 
기술적인 용어나 이름은 번역하지 않고 그대로 사용해 주세요.

# Question: 
{question} 

# Context: 
{context} 

# Answer:"""
)

# 5. Ollama 초기화
llm = ChatOllama(model="qwen3:8b")

# 6. 체인을 생성합니다.
chain = prompt | llm | StrOutputParser()

# 7. chain 실행 및 결과 출력을 반복
while True:
    # 7-1. 사용자의 입력을 기다림
    question = input("\n\n당신: ")
    if question == "끝" or question == "exit":
        break

    # 7-2. 쿼리 처리 (Query-Retriever) : 벡터 DB 에서 참고할 문서 검색
    retrieved_docs = retriever.invoke(question)
    print(f"retrieved size: {len(retrieved_docs)}")
    combined_docs = "\n\n".join(doc.page_content for doc in retrieved_docs)

    # 7-3. 검색된 문서를 첨부해서 PROMPT 생성
    formatted_prompt = {"context": combined_docs, "question": question}

    # 7-4. 체인을 실행하고 결과를 stream 형태로 출력
    result = ""
    for chunk in chain.stream(formatted_prompt):
        print(chunk, end="", flush=True)
        result += chunk
