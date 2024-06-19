from langchain_core.pydantic_v1 import BaseModel, Field


class _StructualInquiryLetter(BaseModel):
    监管问题: str = Field(description='概括需要公司说明的监管问题')
    监管问题背景: str = Field(description='需要公司说明的监管问题的背景')
    需要问询公司的具体方面: str = Field(description='每个监管问题需要问询公司的具体方面，是一个list')
    
    


class StructualInquiryLetter(BaseModel):
    列表: list[_StructualInquiryLetter] = Field(description='所有监管问题的列表')
    问询函主题: str = Field(description='问询函的主旨摘要，格式：“关于XXXX公司XX问题的问询函”')
    问询机构: str = Field(description='证券交易所名称，只能为"上海证券交易所"或"深圳证券交易所"')
    函件类别: str = Field(description='函件的类别')
    公司名称: str = Field(description='公司的名称，为工商信息登记的全称')
    证券代码: str = Field(description='上市公司的证券代码')
    公告日期: str = Field(description='证券交易所发布函件的日期，请把日期转换为阿拉伯数字')


class TaggingInquiryLetter(BaseModel):
    监管问题: str = Field(description='概括需要公司说明的监管问题')
    监管问题背景: str = Field(description='需要公司说明的监管问题的背景')
    需要问询公司的具体方面: str = Field(description='每个监管问题需要问询公司的具体方面，是一个list')
    监管问题类别: str = Field(description='监管问题的类别',
                        enum=[])
    问询函主题: str = Field(description='问询函的主旨摘要，格式：“关于XXXX公司XX问题的问询函”')
    问询机构: str = Field(description='证券交易所名称，只能为"上海证券交易所"或"深圳证券交易所"')
    函件类别: str = Field(description='函件的类别')
    公司名称: str = Field(description='公司的名称，为工商信息登记的全称')
    证券代码: str = Field(description='上市公司的证券代码')
    公告日期: str = Field(description='证券交易所发布函件的日期，请把日期转换为阿拉伯数字')