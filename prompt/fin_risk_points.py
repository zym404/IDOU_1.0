from output_parser.fin_risk_points import FinRiskPoints
from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from core.model_config import EMB
from prompt.examples.fin_risk_points import FIN_RISK_POINTS_EXAMPLES
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from vector_store.Milvus import get_vector_store
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# vector_db = get_vector_store(collection_name='fin_risk_points_prompt_examples')

# example_selector = SemanticSimilarityExampleSelector.from_examples(
#     FIN_RISK_POINTS_EXAMPLES,
#     EMB,
#     vector_db,
#     k=1,
#     # input_keys=["query"],
# )



system_prompt = """
你是一个分析财务报表的专家,下面是这家公司存在的财务异常点，
请你结合已知的异常点信息和异常点对应的话术模板，用中文按照模板分析这个异常点。:
------
以下是这家公司存在的异常点信息
```{abnormal_event}```
------
以下是该异常点信息对应的话术模板
```{script}```
"""

# 用于对格式化prompt





FIN_RISK_POINTS_PROMPT  = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)