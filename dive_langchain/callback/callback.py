from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict, List
from langchain.schema import LLMResult

class CustomCallbackHandler(BaseCallbackHandler):
    """Base callback handler that can be used to handle callbacks from langchain."""
    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""
        # print(prompts)    
        print(f"***Prompt to LLM was:***\n{prompts[0]}")
        print("******")
    
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        # print(response)
        print(f"***LLM response was:***\n{response.generations[0][0].text}")
        print("******")
