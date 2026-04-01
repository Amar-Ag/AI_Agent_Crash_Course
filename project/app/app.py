import streamlit as st
import asyncio
import os
from dotenv import load_dotenv

import ingest
import search_agent
import logs

from pathlib import Path
load_dotenv(Path(__file__).parent.parent.parent / '.env')

REPO_OWNER = "DataTalksClub"
REPO_NAME = "data-engineering-zoomcamp"

@st.cache_resource
def initialize():
    st.write("🔄 Loading Zoomcamp docs and building indexes...")
    index, vindex, embedding_model = ingest.index_data(REPO_OWNER, REPO_NAME)
    agent = search_agent.init_agent(
        index, vindex, embedding_model, REPO_OWNER, REPO_NAME
    )
    st.write("✅ Ready!")
    return agent

agent = initialize()

st.set_page_config(
    page_title="DE Zoomcamp Assistant",
    page_icon="🤖",
    layout="centered"
)
st.title("🤖 Data Engineering Zoomcamp Assistant")
st.caption("Ask me anything about the DataTalksClub Data Engineering Zoomcamp")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask your question about the Zoomcamp..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = asyncio.run(agent.run(user_prompt=prompt))
            answer = response.output
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    logs.log_interaction_to_file(agent, response.new_messages())