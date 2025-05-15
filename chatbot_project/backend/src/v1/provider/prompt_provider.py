from langchain import hub

from langchain_core.prompts import PromptTemplate
from backend.src.v1.model.output_parser import result_parser

def retrieval_qa_prompt_template() -> PromptTemplate:
    template = """
Instructions: Compose a comprehensive reply to the question using the search results given.
If the search result does not relate to the question or no search result is provided,
simply state "No Answer".
Do not use prior knowledge to answer the question.
If the search results mention multiple subjects with the same name, create separate answers for each.
Only include information found in the search result and don't add any additional information.
Make sure the answer is correct and don't output false content.
Ignore outlier search results which has nothing to do with the question.
Only answer what is asked. The answer should be short and concise. Don't add prior knowledge to the answer.
Answer step-by-step.
Don't use prior knowledge to answer.

{format_instructions}


Chat History:
{chat_history}

Current Question:
{question}

Retrieved Context:
{context}

Answer:
"""
    return PromptTemplate(
        input_variables=["chat_history", "question", "context"],
        partial_variables={"format_instructions": result_parser.get_format_instructions()},
        template=template
    )