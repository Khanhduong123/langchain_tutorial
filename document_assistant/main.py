import time
import os
import streamlit as st
from backend.core import run_llm
from typing import List
from typing import List, Dict, Any
from langchain.schema.messages import AIMessage, HumanMessage
from langchain.schema.messages import BaseMessage
st.header("Document Search with Langchain and Pinecone")



def format_chat_history(chat_history: List[BaseMessage]) -> str:
    formatted = []
    for msg in chat_history:
        if isinstance(msg, HumanMessage):
            formatted.append(f"Human: {msg.content}")
        elif isinstance(msg, AIMessage):
            formatted.append(f"AI: {msg.content}")
        else:
            formatted.append(f"System: {msg.content}")
    return "\n".join(formatted)


# Khởi tạo session state
if "chat_answer_history" not in st.session_state:
    st.session_state.chat_answer_history = []
if "user_prompt_history" not in st.session_state:
    st.session_state.user_prompt_history = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Tạo form để xử lý submit và clear input
with st.form("chat_form", clear_on_submit=True):
    prompt = st.text_input("Message", placeholder="Enter your message here...", key="prompt_input")
    submitted = st.form_submit_button("Send")

if submitted and prompt:
    with st.spinner("Searching..."):
        formatted_chat_history = format_chat_history(st.session_state.chat_history)
        result, contexts = run_llm(prompt, chat_history=formatted_chat_history)
        # source = set(doc["page_content"] for doc in result["source_documents"])

        formatted_result = f"{result.answer} \n\n"

        source_contents = set()
        for doc in contexts:
            try:
                source_contents.add(doc.page_content[:1000] + "..." if len(doc.page_content) > 1000 else doc.page_content)
            except AttributeError:
                continue

        if source_contents:
            formatted_result += "\n\n**Sources:**\n"
            for i, content in enumerate(source_contents, start=1):
                formatted_result += f"> [{i}] {content}\n"

        st.session_state.user_prompt_history.append(prompt)
        st.session_state.chat_answer_history.append(formatted_result)
        st.session_state.chat_history.append(HumanMessage(content=prompt)) #List[BaseMessage]
        st.session_state.chat_history.append((AIMessage(content=result.answer)))
        print("Chat history:", st.session_state.chat_history)

# Hiển thị lịch sử chat
if st.session_state.chat_answer_history:
    for response, user_query in zip(st.session_state.chat_answer_history, st.session_state.user_prompt_history):
        st.chat_message("user").markdown(user_query)
        st.chat_message("assistant").markdown(response)
