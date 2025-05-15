from langchain_core.prompts import PromptTemplate
from backend.output_parser import result_parser
# from output_parser import result_parser

def retrieval_qa_prompt_template() -> PromptTemplate:
    template = """
You are an assistant for question-answering tasks. Use the retrieved context and the chat history below to understand what the user wants. 
If the current question is vague (e.g., "what did I say?", "remember what I asked?"), use the most recent user message from the chat history to infer their actual intent.
Prioritize retrieved context if it's relevant. Be concise (max 3 sentences).

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