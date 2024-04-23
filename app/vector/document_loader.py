import os
# langchain의 여러 모듈을 가져옵니다.
from langchain_text_splitters import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser

def load_codes():    
    # Root 경로
    repo_root = "/Users/julio/projects/gpt-projects/langchain/libs"

    # 불러오고자 하는 패키지 경로
    repo_core = repo_root + "/core/langchain_core"
    repo_community = repo_root + "/community/langchain_community"
    repo_experimental = repo_root + "/experimental/langchain_experimental"
    repo_parters = repo_root + "/partners"
    repo_text_splitter = repo_root + "/text_splitters/langchain_text_splitters"
    repo_cookbook = repo_root + "/cookbook"

    # 불러온 문서를 저장할 빈 리스트를 생성합니다.
    py_documents = []

    for path in [repo_core, repo_community, repo_experimental, repo_parters, repo_cookbook]:
        # GenericLoader를 사용하여 파일 시스템에서 문서를 로드합니다.
        loader = GenericLoader.from_filesystem(
            path,  # 문서를 불러올 경로
            glob="**/*",  # 모든 하위 폴더와 파일을 대상으로 함
            suffixes=[".py"],  # .py 확장자를 가진 파일만 대상으로 함
            parser=LanguageParser(
                language=Language.PYTHON, parser_threshold=30
            ),  # 파이썬 언어의 문서를 파싱하기 위한 설정
        )
        # 로더를 통해 불러온 문서들을 documents 리스트에 추가합니다.
        py_documents.extend(loader.load())

    return py_documents


def load_mdxs():
    # TextLoader 모듈을 불러옵니다.
    from langchain_community.document_loaders import TextLoader

    # 검색할 최상위 디렉토리 경로를 정의합니다.
    root_dir = "/Users/julio/projects/gpt-projects/langchain/"

    mdx_documents = []
    # os.walk를 사용하여 root_dir부터 시작하는 모든 디렉토리를 순회합니다.
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 각 디렉토리에서 파일 목록을 확인합니다.
        for file in filenames:
            # 파일 확장자가 .mdx인지 확인하고, 경로 내 '*venv/' 문자열이 포함되지 않는지도 체크합니다.
            if (file.endswith(".mdx")) and "*venv/" not in dirpath:
                try:
                    # TextLoader를 사용하여 파일의 전체 경로를 지정하고 문서를 로드합니다.
                    loader = TextLoader(os.path.join(dirpath, file), encoding="utf-8")
                    # 로드한 문서를 분할하여 documents 리스트에 추가합니다.
                    mdx_documents.extend(loader.load())
                except Exception:
                    # 파일 로드 중 오류가 발생하면 이를 무시하고 계속 진행합니다.
                    pass
    
    return mdx_documents
