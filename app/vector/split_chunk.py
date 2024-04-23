# RecursiveCharacterTextSplitter 모듈을 가져옵니다.
from langchain_text_splitters import Language
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_codes(py_documents):
    # RecursiveCharacterTextSplitter 객체를 생성합니다. 이 때, 파이썬 코드를 대상으로 하며,
    # 청크 크기는 2000, 청크간 겹치는 부분은 200 문자로 설정합니다.
    py_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=2000, chunk_overlap=200
    )

    # py_docs 변수에 저장된 문서들을 위에서 설정한 청크 크기와 겹치는 부분을 고려하여 분할합니다.
    py_docs = py_splitter.split_documents(py_documents)

    return py_docs

def chunk_mdxs(mdx_documents):
    mdx_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)

    # mdx_docs 변수에 저장된 문서들을 위에서 설정한 청크 크기와 겹치는 부분을 고려하여 분할합니다.
    mdx_docs = mdx_splitter.split_documents(mdx_documents)

    return mdx_docs
