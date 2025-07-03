import streamlit as st
from file_converter import *
from backend import *

st.set_page_config(
    page_title="Semantyl",
    page_icon="✨",
    layout="centered",
)

st.title("✨ Semantyl ✨")
st.markdown("""
Welcome to **Semantyl** — your intelligent document question-answering assistant powered by Semantic Search and RAG.  
Upload your documents, ask questions, and get precise, grounded answers from your own data. 🚀
""")

with st.container():
    st.subheader("📂 Upload your files")
    uploaded_files = st.file_uploader(
        label="(PDF, TXT, DOCX)",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True,
    )

def get_file_ids(files):
    return [f.name + str(f.size) for f in files]

if uploaded_files:
    current_file_ids = get_file_ids(uploaded_files)
    previous_file_ids = st.session_state.get("file_ids")

    if current_file_ids != previous_file_ids:
        with st.spinner("⬆️ Processing your documents..."):
            files_as_text = read_files(uploaded_files)
            searcher = SemanticSearch(files_as_text)
            searcher.process_files()
            st.session_state.searcher = searcher
            st.session_state.file_ids = current_file_ids
        st.success("Documents processed successfully!")

# Create columns: one for input, one for button
input_col, btn_col = st.columns([5, 1])

with input_col:
    query = st.text_input("❓ Enter your query here...")

with btn_col:
    # Add some padding above the button to vertically center it with input box
    st.write("")  # empty write adds some vertical space
    ask = st.button("Ask")

if ask:
    if not query:
        st.warning("⚠️ Please enter a question before submitting.")
    elif "searcher" not in st.session_state:
        st.warning("⚠️ Please upload one or more documents before asking a question.")
    else:
        with st.spinner("🔍 Searching your documents..."):
            response = st.session_state.searcher.produce_output(query)
        st.success("Answer found!")
        st.markdown(response)
