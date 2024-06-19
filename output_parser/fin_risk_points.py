from langchain_core.pydantic_v1 import BaseModel, Field

'''
定义了解析财务异常点输出的解释器 FinRiskPoints
'''

class _FinRiskPoints(BaseModel):
    财务异常表现: str = Field(description='财务异常点的描述')
    数据分析: str = Field(description='财务异常表现在哪些数据上')
    
    
class FinRiskPoints(BaseModel):
    财务异常表现列表: list[_FinRiskPoints] = Field(description='所有财务异常表现的列表')
    # 以下皆可套用模板
    exceptional_concerns: str = Field(description='额外的注意事项')
    suggestion_focus: str = Field(description='建议关注的地方')
    risk_cues: str = Field(description='风险提示，需要谨慎评估的地方')

     
