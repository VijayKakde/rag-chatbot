import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="RAG Document Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Document Q&A Chatbot")
st.caption("Upload a PDF and ask questions about it")

with st.sidebar:
    st.header("📄 Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        if st.button("Upload & Process", type="primary", use_container_width=True):
            with st.spinner("Processing PDF..."):
                response = requests.post(
                    f"{API_URL}/upload",
                    files={"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ Done!")
                    st.metric("Pages", data["pages"])
                    st.metric("Chunks", data["chunks"])
                    st.session_state.pdf_uploaded = True
                else:
                    st.error("Upload failed. Try again.")

    st.divider()

    if st.button("📜 Show History", use_container_width=True):
        st.session_state.show_history = True

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_uploaded" not in st.session_state:
    st.session_state.pdf_uploaded = False

if "show_history" not in st.session_state:
    st.session_state.show_history = False

if st.session_state.show_history:
    st.subheader("📜 Chat History")
    response = requests.get(f"{API_URL}/history")
    if response.status_code == 200:
        history = response.json()["history"]
        if history:
            for item in history:
                with st.expander(f"Q: {item['question'][:60]}..."):
                    st.write(f"**Answer:** {item['answer']}")
                    st.caption(f"🕐 {item['timestamp']}")
        else:
            st.info("No history yet.")
    if st.button("← Back to Chat"):
        st.session_state.show_history = False
        st.rerun()

else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 Sources used"):
                    for src in message["sources"]:
                        st.caption(f"📄 Page {src['page']}: {src['preview']}...")

    if not st.session_state.pdf_uploaded:
        st.info("👈 Upload a PDF from the sidebar to get started")

    if question := st.chat_input("Ask a question about your document..."):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": question}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.write(data["answer"])
                    with st.expander("📚 Sources used"):
                        for src in data["sources"]:
                            st.caption(f"📄 Page {src['page']}: {src['preview']}...")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data["answer"],
                        "sources": data["sources"]
                    })
                else:
                    error_msg = "Something went wrong. Make sure a PDF is uploaded first."
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })