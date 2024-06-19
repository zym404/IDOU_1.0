#!/usr/bin/env python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain.prompts import ChatPromptTemplate
from core.model_config import LLM
from langserve import add_routes
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap
from langserve import RemoteRunnable
# from core.agent import agent
from core.model_config import LLM
from core.chain import conversational_rag_chain

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)



prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
add_routes(
    app,
    conversational_rag_chain,
    path="/rag",
)
add_routes(
    app,
    LLM,
    path="/kimi",
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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8002)



    