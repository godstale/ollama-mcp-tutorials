import bs4
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# 1. 문서 로딩 (Document Loading)
loader = WebBaseLoader(
    web_paths=("https://www.bbc.com/korean/articles/cl4yml4l6j1o",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer("div", attrs={"class": ["bbc-1cvxiy9"]})
    ),
)
docs = loader.load()
print(f"문서의 수: {len(docs)}")

# 2. 문서 분할 (Splitting)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.split_documents(docs)
print(f"split size: {len(splits)}")

# 3. 벡터 저장소 구축 (Vector Database)
embeddings = OllamaEmbeddings(model="bge-m3")
vector_store = FAISS.from_documents(documents=splits, embedding=embeddings)
retriever = vector_store.as_retriever()

# 4. LLM 준비
prompt = PromptTemplate.from_template(
    """당신은 질문-답변(Question-Answering)을 수행하는 AI 어시스턴트입니다. 당신의 임무는 주어진 문맥(context) 에서 주어진 질문(question) 에 답하는 것입니다.
검색된 다음 문맥(context) 을 사용하여 질문(question) 에 답하세요. 만약, 주어진 문맥(context) 에서 답을 찾을 수 없다면, 답을 모른다면 `주어진 정보에서 질문에 대한 정보를 찾을 수 없습니다` 라고 답하세요.
질문과 관련성이 높은 내용만 답변하고 추측된 내용을 생성하지 마세요. 기술적인 용어나 이름은 번역하지 않고 그대로 사용해 주세요.
#Question:
{question}
#Context:
{context}
#Answer:"""
)
llm = ChatOllama(model="qwen3:8b", temperature=0)
chain = prompt | llm | StrOutputParser()
question = "극한 호우의 원인은 무엇인가?"

# 5. 벡터 스토어 검색
retrieved_docs = retriever.invoke(question)
print(f"retrieved size: {len(retrieved_docs)}")
combined_docs = "\n\n".join(doc.page_content for doc in retrieved_docs)

# 6. 검색 결과와 프롬프트 구성하여 LLM에 질문
formatted_prompt = {"context": combined_docs, "question": question}
for chunk in chain.stream(formatted_prompt):
    print(chunk, end="", flush=True)
