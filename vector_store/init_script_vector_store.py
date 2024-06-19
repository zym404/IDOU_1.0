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

def init_script_vector_store():
    # files_paths = _get_all_xlsx_files()
    filepath = './docs/话术模板/财务异常点模板.xlsx'
    df = pd.read_excel(filepath)
    texts = excel_splitter(filepath,max_chunk_size=500)
    texts = [str(text) for text in texts]
    # [len(text) for text in texts[:10]]
    # texts[0]
    vector_db = init_vector_store_from_texts(texts,collection_name='script')
    return vector_db


