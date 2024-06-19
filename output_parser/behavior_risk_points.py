from langchain_core.pydantic_v1 import BaseModel, Field

'''
定义了解析财务异常点输出的解释器 BehaviorRiskPoints
'''


class BehaviorRiskPoints(BaseModel):
    行为异常表现列表: str = Field(description='行为异常的表现')
    # 以下皆可套用模板
    行为异常建议: str = Field(description='针对异常点的建议')
    