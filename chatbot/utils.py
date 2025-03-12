import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def kospi():
    KOSPI_URL = 'https://finance.naver.com/sise/'
    res = requests.get(KOSPI_URL)
    selector = '#KOSPI_now'

    soup = BeautifulSoup(res.text, 'html.parser')
    kospi = soup.select_one(selector)
    return kospi.text  # KOSPI 지수 반환

def openai(api_key, user_input):
    client = OpenAI(api_key = api_key)

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "system",
            "content": "넌 챗봇이고 항상 예의 있게 대화해야해."
            }, 
            {
            "role": "user",
            "content": user_input
            }]
    )
    return completion.choices[0].message.content  # OpenAI API 응답 반환

def langchain(user_input):
    llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vector_store = InMemoryVectorStore(embeddings)

    # 1. load document
    loader = WebBaseLoader(
        web_paths=(
            'https://m.sports.naver.com/basketball/article/144/0001024787',
        )
    )
    docs = loader.load()  # 문서 로드

    # 2. split
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    all_splits = text_splitter.split_documents(docs)  # 문서 분할

    # 3. store
    _ = vector_store.add_documents(documents=all_splits)  # 문서 저장

    # 4. retrieve
    prompt = hub.pull('rlm/rag-prompt')
    retrieved_docs = vector_store.similarity_search(user_input)  # 유사한 문서 검색
    docs_content = '\n\n'.join(doc.page_content for doc in retrieved_docs)
    prompt = prompt.invoke({'question': user_input, 'context': docs_content})
    answer = llm.invoke(prompt).content  # 답변 생성

    return answer  # 답변 반환