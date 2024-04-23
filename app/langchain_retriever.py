# langchain_community 모듈에서 FAISS 클래스를 가져옵니다.
from langchain_community.vectorstores import FAISS

# langchain.retrievers 모듈에서 BM25Retriever 클래스를 가져옵니다.
from langchain.retrievers import BM25Retriever

# langchain.retrievers 모듈에서 EnsembleRetriever 클래스를 가져옵니다.
from langchain.retrievers import EnsembleRetriever

def retriever(combined_documents, cached_embeddings):
    FAISS_DB_INDEX = "langchain_faiss"

    # FAISS 클래스의 load_local 메서드를 사용하여 저장된 벡터 인덱스를 로드합니다.
    db = FAISS.load_local(
        FAISS_DB_INDEX,  # 로드할 FAISS 인덱스의 디렉토리 이름
        cached_embeddings,  # 임베딩 정보를 제공
        allow_dangerous_deserialization=True,  # 역직렬화를 허용하는 옵션
    )

    # MMR을 사용하여 검색을 수행하는 retriever를 생성합니다.
    faiss_retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 10})

    # 문서 컬렉션을 사용하여 BM25 검색 모델 인스턴스를 생성합니다.
    bm25_retriever = BM25Retriever.from_documents(
        combined_documents  # 초기화에 사용할 문서 컬렉션
    )

    # BM25Retriever 인스턴스의 k 속성을 10으로 설정하여,
    # 검색 시 최대 10개의 결과를 반환하도록 합니다.
    bm25_retriever.k = 10

    # EnsembleRetriever 인스턴스를 생성합니다.
    # 이때, BM25 검색 모델과 FAISS 검색 모델을 결합하여 사용합니다.
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, faiss_retriever],  # 사용할 검색 모델의 리스트
        weights=[0.6, 0.4],  # 각 검색 모델의 결과에 적용할 가중치
        search_type="mmr",  # 검색 결과의 다양성을 증진시키는 MMR 방식을 사용
    )

    return ensemble_retriever