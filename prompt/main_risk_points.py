from output_parser.main_risk_points import MainRiskPoints
from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

main_risk_points_prompt_template = """
你是一个分析财务报表的专家,请用中文回答我以下问题:
 {question}
------
```{context}```
------
{format_instructions}
"""

# 用于对格式化prompt
# format_instructions_question = PydanticOutputParser(pydantic_object=StructualInquiryLetter)  
main_risk_points_parser = JsonOutputParser(pydantic_object=MainRiskPoints)  


MAIN_RISK_POINTS_PROMPT = PromptTemplate(
    template=main_risk_points_prompt_template, 
    input_variables=["context", "question"],
    partial_variables={"format_instructions":main_risk_points_parser.get_format_instructions()}

)