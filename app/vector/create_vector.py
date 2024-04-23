# langchain_community 모듈에서 FAISS 클래스를 가져옵니다.
from langchain_community.vectorstores import FAISS

def create_vector(combined_documents, cached_embeddings):
    # 로컬에 저장할 FAISS 인덱스의 폴더 이름을 지정합니다.
    FAISS_DB_INDEX = "langchain_faiss"

    # combined_documents 문서들과 cached_embeddings 임베딩을 사용하여
    # FAISS 데이터베이스 인스턴스를 생성합니다.
    db = FAISS.from_documents(combined_documents, cached_embeddings)

    # 생성된 데이터베이스 인스턴스를 지정한 폴더에 로컬로 저장합니다.
    db.save_local(folder_path=FAISS_DB_INDEX)