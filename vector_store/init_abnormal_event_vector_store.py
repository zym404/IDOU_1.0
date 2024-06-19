import os
import pandas as pd

from vector_store.Milvus import init_vector_store_from_texts
from spiliter.excel_spiliter import excel_splitter
from spiliter.csv_spiliter import csv_splitter

# def _get_all_xlsx_files(source_dir='../docs/话术模板'):
#     xlsx_files = []
#     for root, dirs, files in os.walk(source_dir):
#         for file in files:
#             if file.endswith('.xlsx'):
#                 xlsx_files.append(os.path.join(root,file))
#     return xlsx_files

def init_abnormal_event_vector_store(source_dir):
    # 考虑到后续需要使用到多个测试样例，source_dir接受传入的存放异常事件的地址
    # files_paths = _get_all_xlsx_files(source_dir)
    filepath = './docs/IDOU测试样例/03_异常事件触发情况_20231024.xlsx'
    texts = excel_splitter(filepath,max_chunk_size=500)
    texts = [str(text) for text in texts]
    # [len(text) for text in texts[:10]]
    # texts[0]
    vector_db = init_vector_store_from_texts(texts,collection_name='abnormal_event')
    return vector_db
