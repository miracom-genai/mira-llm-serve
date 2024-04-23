from fastapi import Depends, FastAPI, Header, HTTPException
from typing_extensions import Annotated
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Union
from langserve.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langserve import add_routes
from chain import chain
from chat import chain as chat_chain
from translator import chain as EN_TO_KO_chain
from llm import llm as model
from langchain_chain import rag_chain

# async def verify_token(x_token: Annotated[str, Header()]) -> None:
#     """Verify the token is valid."""
#     # Replace this with your actual authentication logic
#     if x_token != "secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")

app = FastAPI(
    title="Miracom LLM Service",
    version="1.0",
    # dependencies=[Depends(verify_token)],
    description="Miracom LLM Service provides a solution to build and deploy customised conversational AI models using your internal data."
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/langchain/playground")


add_routes(app, rag_chain, path="/langchain")

add_routes(app, chain, path="/prompt")


class InputChat(BaseModel):
    """Input for the chat endpoint."""

    messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
        ...,
        description="The chat messages representing the current conversation.",
    )


add_routes(
    app,
    chat_chain.with_types(input_type=InputChat),
    path="/chat",
    enable_feedback_endpoint=True,
    enable_public_trace_link_endpoint=True,
    playground_type="chat",
)

add_routes(app, EN_TO_KO_chain, path="/translate")

add_routes(app, model, path="/llm")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
