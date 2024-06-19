import langchain
import logging
import pandas as pd
from core.model_config import LLM
from core.core_chain import load_chain
from core.output_format_conversion import Json2DataFrame_InquryLetter
from vector_store.Milvus import get_vector_store, VectorCollectionName,return_raw_file,get_all_file_name
from langchain_community.llms.chatglm3 import ChatGLM3
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.schema.messages import AIMessage
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents import initialize_agent, AgentType
from langchain_community.embeddings import QianfanEmbeddingsEndpoint
from langchain_community.llms.baidu_qianfan_endpoint import QianfanLLMEndpoint
from langchain_community.chat_models.baidu_qianfan_endpoint import QianfanChatEndpoint
from langchain_community.chat_models import QianfanChatEndpoint
from PyPDF2 import PdfReader
import time

# 设置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# vector_db = get_vector_store(collection_name=VectorCollectionName)


class DocChatter(object):
    enable_debug = True

    @classmethod
    def enable_debug_mode(cls, is_enable: bool) -> None:
        cls.enable_debug = is_enable
        langchain.debug = is_enable
        logging.info(f"Debug mode set to {'enabled' if is_enable else 'disabled'}.")

    @classmethod
    def StructualInqueryLetter(
        cls, 
        query: str, 
        file_type = '问询函',
        waiting_time = 80,
        ) -> pd.DataFrame:
        '''
        LLM调用有TMP和RPM限制，一分钟内token和request不能超过某一个数量
        结构化任务容易触发这个限制，故出现改情形时，可以适当加大waiting_time参数
        '''
        doc_list = return_raw_file(file_type) # 生成要格式化的文件任务队列
        filename_list = get_all_file_name(file_type) # 生成文件名的任务队列

        llm = LLM
        struc_chain = load_chain(llm=llm,chain_type='stuff', verbose=cls.enable_debug)

        output = ''
        df = pd.DataFrame()
        for i in range(len(doc_list)):
            doc = doc_list[i]
            _query = query.format(inquiry_letter=filename_list[i])
            logging.debug(f"Executing StructualInqueryLetter with query: {_query} and filename: {filename_list[i]}")

            chain = struc_chain({"input_documents": doc, "question": _query},
                        return_only_outputs=cls.enable_debug)
            txt = chain["output_text"]
            output += txt
            try:
                df_tmp = Json2DataFrame_InquryLetter(txt)
                df = pd.concat([df,df_tmp],ignore_index=True)
            except:
                pass
            time.sleep(waiting_time)
        print("使用向量数据库+千帆线上模型")
        print(output)
        return df
    
    @classmethod
    def TaggingInqery(cls, query: str, df_context: pd.DataFrame):
        '''
        使用StructualInqueryLetter返回的DataFrame作为输入，判断每一条记录的监管问题类型
        '''
        context = df_context.to_json(orient='records',force_ascii=False)
        llm = LLM
        label_chain = load_chain(llm=llm,chain_type='label')
        df = df_context
        chain = label_chain
        output = chain.invoke({"question":query,"context":context})
        df_tmp = pd.DataFrame(output)
        df = pd.concat([df,df_tmp],axis=1)
        print("使用向量数据库+千帆线上模型")
        print(output)
        return df
    
    @classmethod
    def GptRagQuery(cls, top_n: int, query: str, file_type:str, using_new_vector_db=True):
        logging.debug(f"Executing GptRagQuery with query: {query} and top_n: {top_n}")
        # 查询相似度向量库
        if using_new_vector_db == True:
            vector_db = create_vector_store(file_type=file_type,collection_name=file_type)
        else:
            vector_db = get_vector_store(collection_name=file_type)
        docs = vector_db.similarity_search(query=query, k=4)
        print(len(docs))
        if len(docs) == 0:
            return print("没有找到相关的文档")
        logging.debug(f"Retrieved top {top_n} documents for query.")
        print('foun oucumnt' + query)
        llm = LLM
        nchain = load_chain(llm=llm, chain_type ="map_reduce",
                            return_map_steps=cls.enable_debug, verbose=cls.enable_debug)
        real = nchain({"input_documents": docs, "question": query + " 用中文回答"},
                      return_only_outputs=cls.enable_debug)
        print("使用向量数据库+千帆线上模型")
        print(real["output_text"])
        return real["output_text"]

    @classmethod
    def VectorQuery(cls, top_n: int, query: str, file_type:str, using_new_vector_db=True):
        logging.debug(f"Executing VectorQuery with query: {query} and top_n: {top_n}")
        # 查询相似度向量库
        if using_new_vector_db == True:
            vector_db = create_vector_store(file_type=file_type,collection_name=file_type)
        else:
            vector_db = get_vector_store(collection_name=file_type)
        docs = vector_db.similarity_search(query=query, k=1)
        print(len(docs))
        if len(docs) == 0:
            return "没有找到相关的文档"
        print("使用向量数据库直接查找")
        logging.debug(f"Retrieved top {top_n} documents for query.")
        return docs[0]


