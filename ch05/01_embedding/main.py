from langchain_ollama import OllamaEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

# 1. 올라마 임베딩 모델들을 사용할 수 있도록 준비
bge_embed = OllamaEmbeddings(model="bge-m3")
nomic_embed = OllamaEmbeddings(model="nomic-embed-text")
llm_embed = OllamaEmbeddings(model="qwen3:8b")

# 2. 사용자로부터 문장 3개를 입력 받음
sentences = [input(f"문장 {i + 1}을 입력하세요: ") for i in range(3)]

# 3. 임베딩 모델 별로 문장 3개에 대한 임베딩 벡터 추출
bge_vectors = [bge_embed.embed_query(sentence) for sentence in sentences]
nomic_vectors = [nomic_embed.embed_query(sentence) for sentence in sentences]
llm_vectors = [llm_embed.embed_query(sentence) for sentence in sentences]

# 4. 문장 벡터 간 코사인 유사도 계산
bge_similarities = cosine_similarity(bge_vectors)
nomic_similarities = cosine_similarity(nomic_vectors)
llm_similarities = cosine_similarity(llm_vectors)

# 5. 문장 간 유사도를 임베딩 모델 별로 화면에 출력
for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        print(f"\n- 문장 {i + 1}과 문장 {j + 1}의 유사도 -")
        print(f"BGE-M3: {bge_similarities[i][j]:.2f}")
        print(f"Nomic-embed-text: {nomic_similarities[i][j]:.2f}")
        print(f"QWEN3: {llm_similarities[i][j]:.2f}")
