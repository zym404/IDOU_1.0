from output_parser.behavior_risk_points import BehaviorRiskPoints
from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from core.model_config import EMB
from prompt.examples.behavior_risk_points import BEHAVIOR_RISK_POINTS_EXAMPLES
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from vector_store.Milvus import get_vector_store
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


vector_db = get_vector_store(collection_name='behavior_risk_points_prompt_examples')

example_selector = SemanticSimilarityExampleSelector.from_examples(
    BEHAVIOR_RISK_POINTS_EXAMPLES,
    EMB,
    vector_db,
    k=1,
    # input_keys=["query"],
)



behavior_risk_points_prompt_template = """
你是一个分析财务报表的专家,请用中文回答我以下问题:
 {question}
------
```{context}```
------
{format_instructions}
"""

# 用于对格式化prompt

behavior_risk_points_parser = JsonOutputParser(pydantic_object=BehaviorRiskPoints)  


BEHAVIOR_RISK_POINTS_PROMPT = PromptTemplate(
    template=behavior_risk_points_prompt_template, 
    input_variables=["context", "question"],
    partial_variables={"format_instructions":behavior_risk_points_parser.get_format_instructions()}

)
# BEHAVIOR_RISK_POINTS_PROMPT = ChatPromptTemplate(
#     [
#         (
#             'System',
#             behavior_risk_points_prompt_template
#         ),
#         MessagesPlaceholder(variable_name='history')
#         ('human','{input}')
#     ],
#     template=behavior_risk_points_prompt_template, 
#     input_variables=["context", "input"],
#     partial_variables={"format_instructions":behavior_risk_points_parser.get_format_instructions()}
# )