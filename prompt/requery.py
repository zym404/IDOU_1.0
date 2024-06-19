from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from core.model_config import EMB
from vector_store.Milvus import get_vector_store
from prompt.examples.requery import REQUERY_EXAMPLES



vector_db = get_vector_store(collection_name='requery_prompt_examples')

example_selector = SemanticSimilarityExampleSelector.from_examples(
    REQUERY_EXAMPLES,
    EMB,
    vector_db,
    k=1,
    # input_keys=["query"],
)

example_prompt = PromptTemplate.from_template("输入的问题: {input}\n重组后的问题: {query}")

REQUERY_PROMPT = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="你现在需要对输入的问题进行重组。",   
    suffix="输入的问题: {input}\n重组后的问题: ",
    input_variables=["input"],
)


# from langchain_community.llms.baidu_qianfan_endpoint import QianfanLLMEndpoint
# llm = QianfanLLMEndpoint(
#     model="ERNIE-Speed-128k",
#     temperature=0.4,
#     )

# chain = REQUERY_PROMPT | llm
# chain.get_prompts()
# chain.invoke({"input": '申通地铁2012年有哪些财务问题为多少'})


