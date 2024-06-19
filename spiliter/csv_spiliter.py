import json
import pandas as pd
from typing import Any, Dict, List, Optional

from langchain_text_splitters import RecursiveJsonSplitter
'''
# 实现读取csv文件并按行进行分割
# 1. 读取csv文件
# 2. 转换为json格式
# 3. 使用RecursiveJsonSplitter进行文本分割
# 4. 输出分割后的文本
'''
def csv_splitter(filepath: str,
                   max_chunk_size: Optional[str]=500,
                   ) -> List[Dict]:

    df = pd.read_csv(filepath,encoding='utf-8')
    txt = df.to_json(orient='records',force_ascii=False)
    json_data = json.loads(txt)

    text_splitter = RecursiveJsonSplitter(max_chunk_size=max_chunk_size)

    json_chunks = text_splitter.split_json(json_data=json_data,convert_lists=True)

    return json_chunks