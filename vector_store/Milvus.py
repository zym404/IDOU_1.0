import openai
import os
from typing import List, Optional
from langchain_milvus.vectorstores import Milvus
# from langchain_community.vectorstores.milvus import Milvus
from langchain_core.vectorstores import VectorStore
from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.docstore.document import Document
from spiliter.pdf_splitter import PdfEngine
from core.model_config import EMB

DocumentPath = "./docs/"
VectorDbHost = "localhost"
VectorDbPort = "19530"
VectorCollectionName = "Inquiry_letter_1"


def get_all_sub_path(source_dir: str = "./docs/", filter_file: str = ""):
    """
    :param source_dir:起始目录
    :param filter_file:取某个后缀的文件，如果没指定则全部都返回
    :return:
    get_all_sub_path 深度遍历目录和子目录并返回文件列表
    """
    path_list = []
    for fpath, dirs, fs in os.walk(source_dir):
        for f in fs:
            p = os.path.join(fpath, f)
            if filter_file != "":
                if p.endswith(filter_file):
                    path_list.append(p)
            else:
                path_list.append(p)

    return path_list

def get_all_file_name(doc_type='问询函',source_dir: str = "./docs/"):
    pdf_files = []
    source_dir += doc_type
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(file.replace('.pdf',''))
    return pdf_files


def init_vector_store_from_documents(
        documents: List[Document],
        collection_name: str = VectorCollectionName,
        ) -> VectorStore:
    '''
    从Document类型的数据集中创建向量库
    '''
    
    vector_db = Milvus.from_documents(
        documents,
        EMB,
        connection_args={"host": VectorDbHost, "port": VectorDbPort},
        collection_name=collection_name,
        drop_old=True,
    )
    return vector_db

def init_vector_store_from_texts(
        texts: List[str],
        collection_name: str = VectorCollectionName,
        ) -> VectorStore:
    '''
    从Document类型的数据集中创建向量库
    '''
    
    vector_db = Milvus.from_texts(
        texts,
        EMB,
        connection_args={"host": VectorDbHost, "port": VectorDbPort},
        collection_name=collection_name,
        drop_old=True,
    )
    return vector_db

# 未使用
def incr_embeddings(documents: List[Document]):
    db = get_vector_store()
    index = db.add_documents(documents)
    return index

# 传入向量数据集的名字，返回对应的数据集
# 以"ragpdf"为例，返回应该是向量数据库服务器上对应的"ragpdf"向量库
def get_vector_store(collection_name: str = VectorCollectionName):

    milvus_store = Milvus(
        embedding_function=EMB,
        collection_name=collection_name,
        connection_args={"host": VectorDbHost, "port": VectorDbPort},
    )
    return milvus_store


def init_vector_store(collection_name: str = VectorCollectionName) -> VectorStore:
    # markdown
    markdownFiles = get_all_sub_path(DocumentPath, ".md")
    print(f"------->>>>>> markdown files {len(markdownFiles)} documents")
    documents = MarkdownHeaderSplitter.batch_split(markdownFiles)
    print(f"------->>>>>> markdown generate {len(documents)} documents")

    # pdf
    pdfFiles = get_all_sub_path(DocumentPath, ".pdf")
    print(f"------->>>>>> pdf files {len(pdfFiles)} documents")
    documents = PdfEngine.batch_split(pdfFiles)
    print(f"------->>>>>> pdf generate {len(documents)} documents")

    return init_vector_store_from_documents(documents, collection_name)


def return_raw_file(file_type):
    # pdf
    pdfFiles = get_all_sub_path(DocumentPath + file_type + '//', ".pdf")
    print(f"------->>>>>> pdf files {len(pdfFiles)} documents")
    documents = PdfEngine.return_raw_file(pdfFiles)
    print(f"------->>>>>> pdf generate {len(documents)} documents")

    return documents
# 未使用
# def test_langchain_chunking(docs_path, splitters, chunk_size, chunk_overlap, drop_collection=True):
#     loader = UnstructuredMarkdownLoader(DocumentPath)
#     docs = loader.load()
#     md_file = docs[0].page_content
#     markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=splitters)
#     md_header_splits = markdown_splitter.split_text(md_file)
#     print(f"------->>>>>> generate {len(md_header_splits)} documents")

#     # Define our text splitter
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#     all_splits = text_splitter.split_documents(md_header_splits)

#     test_collection_name = f"EngineeringNotionDoc_{chunk_size}_{chunk_overlap}"
#     vectordb = Milvus.from_documents(documents=all_splits,
#                                      embedding=EMB,
#                                      connection_args={"uri": "",
#                                                       "token": ""},
#                                      collection_name=test_collection_name)

#     metadata_fields_info = [
#         AttributeInfo(
#             name="Section",
#             description="Part of the document that the text comes from",
#             type="string or list[string]"
#         ),
#     ]
#     document_content_description = "Major sections of the document"
#     llm = QianfanLLMEndpoint(temperature=0)
#     retriever = SelfQueryRetriever.from_llm(llm, vectordb, document_content_description, metadata_fields_info,
#                                             verbose=True)

#     res = retriever.get_relevant_documents("What makes a distinguished engineer?")
#     print(f"""Responses from chunking strategy:
#         {chunk_size}, {chunk_overlap}""")
#     for doc in res:
#         print(doc)
#     # cleanup
#     # this is just for rough cleanup, we can improve this# lots of user considerations to understand for real experimentation use cases thoughif drop_collection:
#     # connections.connect(uri=zilliz_uri, token=zilliz_token)
#     # utility.drop_collection(test_collection_name)

