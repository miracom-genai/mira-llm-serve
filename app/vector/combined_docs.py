from . import document_loader, split_chunk
# from split_chunk import chunk_codes, chunk_mdxs

def create_com_docs():
    py_documents = document_loader.load_codes()
    mdx_documents = document_loader.load_mdxs()

    # 최종적으로 불러온 문서의 개수를 출력합니다.
    print(f".py 파일의 개수: {len(py_documents)}")
    print(f".mdx 파일의 개수: {len(mdx_documents)}")

    py_docs = split_chunk.chunk_codes(py_documents)
    mdx_docs = split_chunk.chunk_mdxs(mdx_documents)

    # 분할된 텍스트의 개수를 출력합니다.
    print(f"분할된 .py 파일의 개수: {len(py_docs)}")
    print(f"분할된 .mdx 파일의 개수: {len(mdx_docs)}")

    combined_documents = py_docs + mdx_docs
    print(f"총 도큐먼트 개수: {len(combined_documents)}")

    return combined_documents
