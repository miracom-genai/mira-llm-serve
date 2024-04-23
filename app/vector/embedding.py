# langchain_openai와 langchain의 필요한 모듈들을 가져옵니다.
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore

def cached_embedding():
    # 로컬 파일 저장소를 사용하기 위해 LocalFileStore 인스턴스를 생성합니다.
    # './cache/' 디렉토리에 데이터를 저장합니다.
    store = LocalFileStore("./cache/")

    # OpenAI 임베딩 모델 인스턴스를 생성합니다. 모델명으로 "text-embedding-3-small"을 사용합니다.
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small", disallowed_special=())

    # CacheBackedEmbeddings를 사용하여 임베딩 계산 결과를 캐시합니다.
    # 이렇게 하면 임베딩을 여러 번 계산할 필요 없이 한 번 계산된 값을 재사용할 수 있습니다.
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
        embeddings, store, namespace=embeddings.model
    )

    return cached_embeddings