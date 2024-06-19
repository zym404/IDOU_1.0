import os
import json
import pandas as pd
import logging

from core.model_config import LLM
from prompt.fin_risk_points import FIN_RISK_POINTS_PROMPT
from vector_store.init_script_vector_store import init_script_vector_store
from vector_store.Milvus import get_vector_store
from spiliter.excel_spiliter import excel_splitter
from vector_store.init_abnormal_event_vector_store import init_abnormal_event_vector_store

from langchain_community.document_transformers import LongContextReorder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables.passthrough import (
                RunnableAssign,
                RunnableParallel,
            )

# 后续考虑不以常量传输llm
llm = LLM

os.environ["LANGCHAIN_TRACING_V2"] = "true"  
os.environ["LANGCHAIN_PROJECT"] = "DateKiller_1.0"  
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"  
os.environ["LANGCHAIN_API_KEY"] = "ls__4e4954be6c504e5f8bd17bf19e0a8396"  # 更新为您的API密钥

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# vector_store_script = init_script_vector_store()
# vector_store_abnormal_event = init_abnormal_event_vector_store('test')
vector_store_abnormal_event = get_vector_store('abnormal_event')
vector_store_script = get_vector_store('script')

retriever_abnormal_event = vector_store_abnormal_event.as_retriever(search_kwargs={'k':15})
retriever_script = vector_store_script.as_retriever(search_kwargs={'k':1})

reordering = LongContextReorder()

contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

retriever_abnormal_event = create_history_aware_retriever(
    llm, retriever_abnormal_event, contextualize_q_prompt
)
retriever_script = create_history_aware_retriever(
    llm, retriever_script, contextualize_q_prompt
)

chain = RunnableAssign(RunnableParallel({'abnormal_event':retriever_abnormal_event,'script':retriever_script})) |FIN_RISK_POINTS_PROMPT |llm

'''
chian的工作机制
1. 输入的字典：{'input':'foo','chat_history':'bar'}
2. RunnableAssign向输入的字典加入新的键：'abnormal_event'和'script'，这两个键接受各自的retriever的值
3. 字典变成了{'input':'foo','chat_history':'bar','abnormal_event':'baz','script':'qux'}
4. 字典传入Prompt，再传入llm，最终输出
'''

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


conversational_rag_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)


# input = "有什么收入异常"
# input = "我刚刚问了什么问题"
# output = conversational_rag_chain.invoke(
#     {"input":input,},
#     config={"configurable": {"session_id": "abc123"}},
# )



