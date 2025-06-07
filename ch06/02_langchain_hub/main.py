import bs4
from dotenv import load_dotenv
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

load_dotenv()  # .env 파일 로드

# 1. 뉴스 URL
news_url = """https://www.bbc.com/korean/articles/c166p510n79o"""

# 2. 뉴스 스크래핑
loader = WebBaseLoader(
    web_paths=([news_url]),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            "div",
            attrs={"class": ["bbc-1cvxiy9", "bbc-fa0wmp"]},
        )
    ),
)
news_array = loader.load()
news = news_array[0]

# 3. 요약에 사용할 프롬프트 불러오기
prompt = hub.pull("hellollama/news_summary")

# 4. Ollama 초기화
llm = ChatOllama(model="qwen3:8b", temperature=0)

# 5. 프롬프트를 실행할 체인생성
summary_chain = prompt | llm | StrOutputParser()

# 6. LLM에 질문
for chunk in summary_chain.stream({"news": news}):
    print(chunk, end="", flush=True)
