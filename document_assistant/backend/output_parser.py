from typing import Any, Dict, List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class Result(BaseModel):
    query: str = Field(description="The original query.")
    answer: str = Field(description="The answer to the query.")
    source_documents: List[Dict[str, Any]] = Field(description="The source documents used to generate the answer.")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "answer": self.answer,
            "source_documents": self.source_documents
        }
    
result_parser = PydanticOutputParser(pydantic_object=Result)