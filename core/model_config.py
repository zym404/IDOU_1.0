import os
from langchain_community.embeddings.baidu_qianfan_endpoint import QianfanEmbeddingsEndpoint
from langchain_community.llms.baidu_qianfan_endpoint import QianfanLLMEndpoint
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# 设置 API 密钥

os.environ["QIANFAN_AK"] = "gKMOfVu47gp3BMMUJb8EPpfG"
os.environ["QIANFAN_SK"] = "1G5RdeXf9RdIjj6bzeF4A1udqT8jTEPl"

LLM = ChatOpenAI(
    openai_api_base="https://api.moonshot.cn/v1/", 
    openai_api_key="sk-F2JsFeY0wKLRIDtnlL9JABWGYa9wvtqh1kIppvhO4PFMxsk9",
    model_name="moonshot-v1-8k",
    temperature=0.6,
    # max_tokens=8096,
    timeout=301.0
)
# LLM = QianfanLLMEndpoint(
#     model="ERNIE-Speed-128k",
#     temperature=0.1,
#     )

EMB = QianfanEmbeddingsEndpoint(model="bge-large-zh") # 每个文本token数不超过512且长度不超过2000个字符
# EMB = QianfanEmbeddingsEndpoint(model="Embedding-V1") # 每个文本token数不超过384且长度不超过1000个字符


# 效果比ERNIE-Speed-128k好，但很容易出现超token的情况
# LLM = QianfanLLMEndpoint(
#     model="ERNIE-3.5-8K",
#     temperature=0.1,
#     )

# 一下代码可查看千帆支持的所有模型
# import qianfan
# qianfan.ChatCompletion().models()