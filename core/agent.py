import os
from typing import Dict, List, Optional, Tuple, Type, Union, cast
from vector_store.Milvus import (
    get_vector_store, 
    VectorCollectionName,
    return_raw_file,
    get_all_file_name,
    init_vector_store,
    create_embeddings_from_documents
)
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from prompt.prmopt_agents import PROMPT
from langchain_community.llms.baidu_qianfan_endpoint import QianfanLLMEndpoint
from langchain.agents import initialize_agent, Tool
from langchain.tools import tool
from langchain.agents import AgentType
from langchain.agents.react.base import DocstoreExplorer
from langchain import (
    LLMMathChain,
    OpenAI,
    SerpAPIWrapper,
    SQLDatabase,
)
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.agents import load_tools
from langchain.document_loaders import WebBaseLoader
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain.tools import DuckDuckGoSearchRun
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from prompt.requery import REQUERY_PROMPT
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# 设置 API 密钥


llm = ChatOpenAI(
    openai_api_base="https://api.moonshot.cn/v1/", 
    openai_api_key="sk-F2JsFeY0wKLRIDtnlL9JABWGYa9wvtqh1kIppvhO4PFMxsk9",
    model_name="moonshot-v1-8k",
    temperature=0.6,
    # max_tokens=8096,
    timeout=301.0
)

os.environ["LANGCHAIN_TRACING_V2"] = "true"  
os.environ["LANGCHAIN_PROJECT"] = "IDOU_1.0"  
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"  
os.environ["LANGCHAIN_API_KEY"] = "ls__4e4954be6c504e5f8bd17bf19e0a8396"  


vector_db = init_vector_store(collection_name='agent')

# import qianfan
# qianfan.ChatCompletion().models()
db = SQLDatabase.from_uri('mysql+pymysql://root:123456@localhost/datakiller')

localDB = RetrievalQA.from_chain_type(
    llm=llm, chain_type='stuff',retriever=vector_db.as_retriever()
)

llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

loader = WebBaseLoader("https://vip.kingdee.com/article/43092414060625972?productLineId=11&lang=zh-CN")

text_splitter = CharacterTextSplitter(        
    separator = "",
    chunk_size = 500,
    chunk_overlap  = 200,
    length_function = len,
)
text = text_splitter.split_documents(loader.load())


fin = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff", retriever=create_embeddings_from_documents(text,collection_name='text').as_retriever()
)


@tool
def SQLDB(query):
    '''
    在查询财务数据时使用，尤其是遇到到localDB查不到的数据时
    '''
    import pymysql
    func = create_sql_query_chain(llm, db)
    response = func.invoke({"question": query})
    response = response.replace('```sql','')
    response = response.replace('```','')
    try:
        return db.run(response)
    except :
        return f"请尝试重组以下问题：{query}"

@tool
def DDGSearch(query): 
    '''
    用于检索网络信息
    '''
    from duckduckgo_search import DDGS
    max_results = 5,
    region = 'cn-zh',
    ddgs_engine = DDGS(proxy='http://localhost:7890')
    results = ddgs_engine.text(query,
                               max_results=5,
                               region=region)
    return str(results)

@tool
def OpenURL():
    '''
    用于打开URL链接
    '''
    pass

@tool
def reQuery(query):
    '''
    在找不到答案时，可能是问题的问法有问题，需要重组问题
    reQuery用于重组问题
    '''
    chain = REQUERY_PROMPT | llm
    return chain.invoke({'input':query,'query':'None'})

tools = [
    # Tool(
    #     name='localDB',
    #     func=localDB.invoke,
    #     description='在查询数据时使用'
    # ),

    # Tool(
    #     name='财务指标',
    #     func=fin.invoke,
    #     description='在查找要计算的财务指标的计算方法时使用'
    # ),
    # SQLDB,
    # reQuery,
    DDGSearch
]



agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
}
memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

agent = initialize_agent(
    tools, 
    llm, 
#    prompt=PROMPT,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    agent_kwargs=agent_kwargs, 
    max_iterations=10,
    memory=memory,
)


agent.invoke('股票代码为000003.SZ的公司2012年的资产负债率为多少，用中文问答')
