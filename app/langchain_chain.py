import os
import time
from vector.combined_docs import create_com_docs
from vector.embedding import cached_embedding
from vector.create_vector import create_vector
from langchain_retriever import retriever

from langchain_core.prompts import PromptTemplate

from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.callbacks.manager import CallbackManager
from langchain_core.runnables import ConfigurableField
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "langchain-ai-" + str(time.time())

# Step I.
combined_documents = create_com_docs()

cached_embeddings = cached_embedding()
create_vector(combined_documents, cached_embeddings)

ensemble_retriever = retriever(combined_documents, cached_embeddings)

# Step II.

prompt = PromptTemplate.from_template(
    """당신은 20년차 AI 개발자입니다. 당신의 임무는 주어진 질문에 대하여 최대한 문서의 정보를 활용하여 답변하는 것입니다.
문서는 Python 코드에 대한 정보를 담고 있습니다. 따라서, 답변을 작성할 때에는 Python 코드에 대한 상세한 code snippet을 포함하여 작성해주세요.
최대한 자세하게 답변하고, 한글로 답변해 주세요. 주어진 문서에서 답변을 찾을 수 없는 경우, "문서에 답변이 없습니다."라고 답변해 주세요.
답변은 출처(source)를 반드시 표기해 주세요.

#참고문서:
{context}

#질문:
{question}

#답변: 

출처:
- source1
- source2
- ...                             
"""
)

# Step III.

class StreamCallback(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs):
        print(token, end="", flush=True)


llm = ChatOllama(
    # model="EEVE-Korean-10.8B:latest",
    model="llama3:latest",
    temperature=0,
    streaming=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
).configurable_alternatives(
    # 이 필드에 id를 부여합니다.
    # 최종 실행 가능한 객체를 구성할 때, 이 id를 사용하여 이 필드를 구성할 수 있습니다.
    ConfigurableField(id="llm"),
    # 기본 키를 설정합니다.
    default_key="ollama",
    gpt3=ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        streaming=True,
        callbacks=[StreamCallback()],
    ),
    gp4=ChatOpenAI(
        model="gpt-4-turbo-preview",
        temperature=0,
        streaming=True,
        callbacks=[StreamCallback()],
    ),
    claude=ChatAnthropic(
        model="claude-3-opus-20240229",
        temperature=0,
        streaming=True,
        callbacks=[StreamCallback()],
    ),
)

# Step IV.

rag_chain = (
    {"context": ensemble_retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# answer = rag_chain.with_config(configurable={"llm": "gpt4"}).invoke(
#     "PromptTemplate 사용방법을 알려주세요"
# )

# print(answer)