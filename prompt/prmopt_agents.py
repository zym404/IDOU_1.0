# flake8: noqa
from langchain_core.prompts.prompt import PromptTemplate

_PROMPT_TEMPLATE = """
将数学问题转换为可以使用Python语言书写的表达式，该表达式可以被numexpr库执行。用运行此代码的输出来回答问题。

Question: ${{含有数学问题的问题}}
```text
${{能解决问题的一行数学表达式}}
```
...numexpr.evaluate(text)...
```output
${{运行代码的输出}}
```
Answer: ${{答案}}

Begin.

Question: 37593 * 67是多少?
```text
37593 * 67
```
...numexpr.evaluate("37593 * 67")...
```output
2518731
```
Answer: 2518731

Question: 37593^(1/5)
```text
37593**(1/5)
```
...numexpr.evaluate("37593**(1/5)")...
```output
8.222831614237718
```
Answer: 8.222831614237718

Question: {question}
"""

PROMPT = PromptTemplate(
    input_variables=["question"],
    template=_PROMPT_TEMPLATE,
)
