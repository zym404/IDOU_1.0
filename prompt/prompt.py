from langchain.output_parsers import PydanticOutputParser
from output_parser.output_parser import StructualInquiryLetter,TaggingInquiryLetter
from langchain.prompts import PromptTemplate
from langchain.prompts import FewShotPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


structual_prompt_template = """你是一个分析财务报表的专家,请用中文回答我以下问题:
 {question}
------
```{context}```
------
{format_instructions}
"""

# 用于对格式化prompt
# format_instructions_question = PydanticOutputParser(pydantic_object=StructualInquiryLetter)  
structual_parser = JsonOutputParser(pydantic_object=StructualInquiryLetter)  


STRUCTUAL_PROMPT = PromptTemplate(
    template=structual_prompt_template, 
    input_variables=["context", "question"],
    partial_variables={"format_instructions":structual_parser.get_format_instructions()}

)



tagging_prompt_template = """你是一个分析财务报表的专家,请用中文回答我以下问题:
 {question}
------
```{context}```
------
监管问题类别如下json所示
{examples}
------
{format_instructions}
"""

tagging_paser = JsonOutputParser(pydantic_object=TaggingInquiryLetter) 
TAGGING_PROMPT = PromptTemplate(
    template=tagging_prompt_template, 
    input_variables=["context", "question",],
    partial_variables={"format_instructions":tagging_paser.get_format_instructions(),
                       "examples": EXAMPLES}
)


struc_prompt_template = """你是一个分析财务报表的专家,请用中文回答我以下问题:
 {question}
------
```{context}```
------
"""

QUESTION_PROMPT = PromptTemplate(
    template=struc_prompt_template, 
    input_variables=["context", "question"],
    
)

combine_prompt_template = """请以以下格式回答问题
Final Answer :

问题: {question}
```{summaries}```"""

COMBINE_PROMPT = PromptTemplate(
    template=combine_prompt_template, input_variables=["summaries", "question"]
)