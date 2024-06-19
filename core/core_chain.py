from langchain.schema.language_model import BaseLanguageModel
from langchain.callbacks.base import BaseCallbackManager
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from typing import Any, Optional
from langchain.chains.question_answering import load_qa_chain
from prompt.prompt import QUESTION_PROMPT, COMBINE_PROMPT, LABEL_PROMPT, STRUCTUAL_PROMPT
from prompt.prompt import label_paser



def load_chain(
        llm: BaseLanguageModel,
        chain_type: str,
        verbose: Optional[bool] = None,
        callback_manager: Optional[BaseCallbackManager] = None,
        **kwargs: Any,
) -> BaseCombineDocumentsChain:

    if chain_type == "stuff":
        return load_qa_chain(
            llm=llm,
            chain_type=chain_type,
            verbose=verbose,        
            prompt=STRUCTUAL_PROMPT,
            callback_manager=callback_manager, **kwargs
        )
    elif chain_type == "map_reduce":
        return load_qa_chain(
            llm=llm,
            chain_type=chain_type,
            verbose=verbose,        
            question_prompt=QUESTION_PROMPT,
            combine_prompt=COMBINE_PROMPT,
            callback_manager=callback_manager, **kwargs
        )
    elif chain_type == "label":
        # 根据对应的字段打标签
        return TAGGING_PROMPT | llm | tagging_paser


