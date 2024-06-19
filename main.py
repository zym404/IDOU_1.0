from fastapi import FastAPI
from core.qa_chain_qianfan import DocChatter
from vector_store.Milvus import init_vector_store, get_vector_store

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/init")
async def init():
    # load documents
    DocChatter.enable_debug_mode(True)
    get_vector_store()
    init_vector_store()
    return {"message": "Hello World"}

@app.post("/chatgpt")
async def chat(params: dict) -> dict:
    query = params["question"]
    # 记录日志
    print(query)
    answer = DocChatter.GptRagQuery(
        top_n=2,
        query=query
    )
    return {"question": query, "answer": answer}

@app.post("/chatvector")
async def chat(params: dict) -> dict:
    query = params["question"]
    # 记录日志
    print(query)
    answer = DocChatter.VectorQuery(
        top_n=2,
        query=query
    )
    return {"question": query, "answer": answer}

@app.post("/localquery")
async def chat(params: dict) -> dict:
    query = params["question"]
    # 记录日志
    print(query)
    answer = DocChatter.LocalQuery(
        top_n=2,
        query=query
    )
    return {"question": query, "answer": answer}

@app.post("/agentmysql")
async def chat(params: dict) -> dict:
    query = params["question"]
    # 记录日志
    print(query)
    answer = DocChatter.LocalQueryMysql(
        top_n=2,
        query=query
    )
    return {"question": query, "answer": answer}