# # 暂时无法使用，待完善！

# import subprocess
# from typing import Any, Optional

# def curl_command(
#         query:str,
#         mode:Optional[str] = 'chatgpt',
#         host:Optional[str] = '8000',
# ) -> str:
#     data = {
#     "question": {query},
#     "style": "text"
#     }
#     return f'''
#     curl --location "http://127.0.0.1:{host}/{mode}" 
#     --header "Content-Type: application/json" 
#     --data "{data}"
#     '''
# query = '''

# 隐性关联方交易的定义为:隐性关联交易，即企业利用税收政策不完备、不明确之处，刻意模糊关联方或交易活动，人为将关联交易“非关联化”，从而免于向税务部门申报，进而掩盖其中隐含的税收问题。

# 请回答以excel表格的形式回答以下问题，表格的列名为['公司','是否存在隐性关联方','判断依据']

# 问题：贵人鸟存在隐性关联方吗？如果存在的话给出判断依据，不存在则不用给出。
# '''
# curl_command('1')
# print(curl_command(query))
# output = subprocess.check_output('curl http://127.0.0.1:8000/chatgpt',shell=True,)
# output = output.decode('utf-8')
# print(output)

