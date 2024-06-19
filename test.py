import os
from core.qa_chain_qianfan import DocChatter

# LangSmith追踪
os.environ["LANGCHAIN_TRACING_V2"] = "true"  
os.environ["LANGCHAIN_PROJECT"] = "DateKiller_1.0"  
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"  
os.environ["LANGCHAIN_API_KEY"] = "ls__4e4954be6c504e5f8bd17bf19e0a8396"  # 更新为您的API密钥

query_1 = '''
证券交易所问询函的结构为总分结构：先总述一个"大的问询事项"，再分述"需要公司说明的监管问题"。在每个"监管问题"中，先总述"监管问题的背景"，再分述每个问题"需要问询公司的具体方面"
以下文本是{inquiry_letter}，你需要将问询函按照"监管问题"字段整理成json的格式输出，json对象的数量和监管问题的数量保持一致
下面是你要做的步骤
0. 创建一个json对象，必须有这些字段: 监管问题、监管问题背景、需要问询公司的具体方面、问询函主题、问询机构、函件类别、公司名称、证券代码、公告日期。
1. 总结一下**整个文本**的主旨概要，存入"问询函主题"字段
2. 将函件按照问询函结构拆分成两部：大的问询事项和需要公司说明的监管问题
3. 总结大的问询事项的主要内容，存入"监管问题"字段
4. 将需要公司说明的监管问题的部分拆分成具体的监管问题
5. 对每个监管问题进行拆分，再拆分出监管问题背景和需要问询公司的具体方面，
6. 把监管问题背景存入"监管问题背景"字段
7. 对需要问询公司的具体方面继续拆分，拆分成一个list，存入"需要问询公司的具体方面"字段
8. 从整个问询函中查询问询机构、函件类别、公司名称、证券代码、公告日期，存入相应的字段

注意：文本是由pdf解析器解析而来，故字符与字符之间存在不必要的空格，请不要输出这些空格
请不要输出和json格式无关的文本，遇到查询不到请填写"未知"
Think step by step
'''

# query_2 = '''
# 经格式化整理后输出的Json问询函文本，你下面要做：
# 1. 计算Json文本中对象数量，记为x
# 2. 根据文本中每条记录的"监管问题背景"和"需要问询公司的具体方面"字段，判断每个监管问题类型
# 3. 如果无法判断，就输出"其他"
# 4. 输出x条"编号"和"监管问题类型"记录，**输出的顺序和Json文本中每条记录排列的顺序一致**

# '''

query_2 = '''
经格式化整理后输出的Json问询函文本，你下面要做：
1. 遍历Json文本中的每个对象
2. 对每个对象，根据"监管问题背景"和"需要问询公司的具体方面"关键字，判断监管问题类型，保存入"监管问题类型"关键字
3. 把"监管问题类型"键值对添加入对象中，生成一个新的对象，并替换原来的对象
4. 遍历完成后，输出新的Json文本

'''


df = DocChatter.StructualInqueryLetter(query=query_1)
df_1 = DocChatter.TaggingInqery(query=query_2,df_context=df)
a = DocChatter.GptRagQuery(query='贵人鸟2021年到2023年每年净利润增长率为多少',top_n=4)
df_1.to_excel('test.xlsx')



# del excel_splitter
# from spiliter.excel_spiliter import excel_splitter

# risk_points = excel_splitter(r'./docs/IDOU测试样例/03_异常事件触发情况_20231024.xlsx',max_chunk_size=1000)
# type(excel_splitter(r'./docs/IDOU测试样例/03_异常事件触发情况_20231024.xlsx',max_chunk_size=1000))
# len(risk_points)
# risk_points[0]