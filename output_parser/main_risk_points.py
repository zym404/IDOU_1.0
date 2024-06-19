from langchain_core.pydantic_v1 import BaseModel, Field


class _MainRiskPoints(BaseModel):
    异常表现分析: str = Field(description='该异常点的具体表现')
    智评提示: str = Field(description='此类公司存在的问题以及需要关注的地方')
    
    
class MainRiskPoints(BaseModel):
    主要风险点列表: list[_MainRiskPoints] = Field(description='所有异常点的列表')
     
