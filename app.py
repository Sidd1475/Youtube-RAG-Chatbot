import streamlit as st
import os
from src.pipeline.rag_pipeline import RAGPipeline


st.set_page_config(page_title="Youtube RAG Chatbot")

st.title("Youtube RAG Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pipeline" not in st.session_state:
    st.session_state.pipeline = RAGPipeline(
        api_key = st.secrets["GEMINI_API_KEY"]
    )
# Track processed video
if "current_video" not in st.session_state:
    st.session_state.current_video = None

pipeline = st.session_state.pipeline 

# UI Inputs
language = st.selectbox("🌐 Select Subtitle Language", ["en", "hi"])
video_id = st.text_input("📺 Enter YouTube Video ID")
query = st.chat_input("Ask something about the video...")

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ⏱ Time formatter
def format_time(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"

# Query flow
if video_id and query:
    # Ensure query is processed 
    
    if st.session_state.current_video != video_id:
        with st.spinner("⏳ Processing video... this may take a few seconds"):
            pipeline.process_video(video_id.strip(), language)
            st.session_state.current_video = video_id

        st.success("✅ Video processed and ready!")
    
    # Store user message
    st.session_state.messages.append({
        "role":"user",
        "content":query
    })
    
    with st.chat_message("user"):
        st.markdown(query)

     # generate answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, sources = pipeline.query(
                query,
                history=st.session_state.messages
            )

        if "Model is currently busy" in answer:
            st.warning(answer)
        elif "Something went wrong" in answer:
            st.error(answer)
        else:
            st.markdown(answer)
            
    # show sources
    if sources:
        with st.expander("Sources"):
            for s in sources:
                text = s["text"]
                if isinstance(text, list):
                    text = " ".join(text)

                st.markdown(
                    f"""
        **⏱ {format_time(s['start'])} - {format_time(s['end'])}**

        {text[:300]}...
        """
                )
                st.divider()
    
    # store assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })