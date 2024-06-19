## DataKiller 1.0（千帆）
** 测试在test.py中进行！！！**

#### 核心文件：

- core_chain.py
  - summarize的chain，后续会改写
- qa_chain_qianfan.py
  - DocChatter
    - GptRagQuery
    - StructualInqueryLetter
    - TaggingInqery
    - VectorQuery
- pdf_splitter.py
- vector_db_qianfan.py

#### 部署命令(暂不支持)
```shell
# https://python.langchain.com/docs/integrations/toolkits/openapi#lets-see-some-examples

uvicorn main:app --port 8000
```

#### 示例
```shell
curl --location "http://127.0.0.1:8002/chatgpt" \
--header "Content-Type: application/json" \
--data "{
    "question": "大豆补贴范围是什么？",
    "style": "text"
}"

# win使用curl时需要对data中每个双引号进行转义！
curl --location "http://127.0.0.1:8002/chatgpt" 
--header "Content-Type: application/json" 
--data "{
\"question\": \"1\",
\"style\": \"text\"
}"
请对贵人鸟打上【是否涉及隐性关联方交易】的标签，并说明为什么具有隐性关联方交易的原因。隐性关联方交易的定义为:隐性关联交易，即企业利用税收政策不完备、不明确之处，刻意模糊关联方或交易活动，人为将关联交易“非关联化”，从而免于向税务部门申报，进而掩盖其中隐含的税收问题。
curl --location "http://127.0.0.1:8000/localquery" \
--header "Content-Type: application/json" \
--data "{
    "question": "请对对企业打上【是否涉及隐性关联方交易】的标签，并说明为什么具有隐性关联方交易的原因。隐性关联方交易的定义为:隐性关联交易，即企业利用税收政策不完备、不明确之处，刻意模糊关联方或交易活动，人为将关联交易“非关联化”，从而免于向税务部门申报，进而掩盖其中隐含的税收问题。",
    "style": "text"
}"

curl --location "http://127.0.0.1:8000/agentmysql" \
--header "Content-Type: application/json" \
--data "{
    "question": "在student库中，表student，查询学生姓名（name）、年龄（age）和成绩（score），首先按照成绩从大到小排序，如果成绩相同，则按照年龄从小到大排序。根据上面信息生成一条sql语句",
    "style": "text"
}"

curl --location "http://127.0.0.1:8000/agentmysql" \
--header "Content-Type: application/json" \
--data "{
    "question": "gva中表user_files的结构是怎样的？不用说废话",
    "style": "text"
}"

export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_ENDPOINT="<https://api.smith.langchain.com>"
export LANGCHAIN_API_KEY="ls__b04e3a33a1ef40cfb2cdf83ad96daaf8"
export LANGCHAIN_PROJECT="langchain_for_llm_application_development"

# ls__b04e3a33a1ef40cfb2cdf83ad96daaf8

```
