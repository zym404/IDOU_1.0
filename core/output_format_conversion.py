import json
import pandas as pd
import re

def Json2DataFrame_InquryLetter(txt:str) -> pd.DataFrame:
    matches = re.findall(r'```json(.*?)```',txt , re.DOTALL)[0].replace('\n','')
    json_script = json.loads(matches)
    df = pd.DataFrame(json_script['列表'])
    lst = ['问询函主题','问询机构','函件类别','公司名称','证券代码','公告日期']
    for x in lst:
        df[x] = json_script[x]
    return df


