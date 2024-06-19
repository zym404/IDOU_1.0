import json
import pandas as pd
from typing import Any, Dict, List, Optional
from copy import deepcopy
import pickle
import requests
from langchain_text_splitters import RecursiveJsonSplitter
'''
# note: 
# RecursiveJsonSplitter的方法存在一些问题，在无法明确被分割对象中嵌套的数据结构时，
# 递归分割会导致可变对象发生不可控变化

'''
def excel_splitter(filepath: str,
                   max_chunk_size: Optional[str]=500,
                   ) -> List[Dict]:
    # filepath = r'./docs/IDOU测试样例/03_异常事件触发情况_20231024.xlsx'
    # max_chunk_size=1000
    # qianfan每个文本token数不超过384且长度不超过1000个字符
    df = pd.read_excel(filepath)
    txt = df.to_json(orient='records',force_ascii=False)
    json_data = json.loads(txt)
    
    return json_data




