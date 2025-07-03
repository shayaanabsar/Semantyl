import streamlit as st
from file_converter import *
from backend import *

st.set_page_config(
    page_title="Semantyl",
    page_icon="✨",
    layout="centered",
)

# --- Custom CSS for subtle styling ---
st.markdown("""
<style>
    /* Page background and container */
    .main {
        background-color: #fafafa;
        padding: 2rem 1.5rem;
        max-width: 700px;
        margin: auto;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgb(0 0 0 / 0.05);
    }
    /* Title styling */
    .title {
        font-weight: 800;
        font-size: 2.8rem;
        color: #5b2eeb;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    /* Subtitle styling */
    .subtitle {
        font-size: 1.1rem;
        color: #555555;
        text-align: center;
        margin-bottom: 2rem;
        line-height: 1.4;
    }
    /* Styled text input */
    div.stTextInput > label {
        font-weight: 600;
        color: #5b2eeb;
        font-size: 1.1rem;
        margin-bottom: 0.4rem;
    }
    /* File uploader label */
    div.stFileUploader > label {
        font-weight: 600;
        color: #5b2eeb;
        font-size: 1.1rem;
        margin-bottom: 0.6rem;
    }
    /* Response box */
    .response-box {
        background: #fff;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 0 15px rgba(91, 46, 235, 0.15);
        color: #333;
        font-size: 1.05rem;
        line-height: 1.5;
        white-space: pre-wrap;
        margin-top: 1.6rem;
        border: 1px solid #ddd;
    }
    /* Success message styling */
    div.stAlertSuccess {
        border-radius: 10px;
        font-weight: 600;
        color: #317a00;
        background-color: #dbf5c6;
        border: 1px solid #a7d233;
        padding: 0.8rem 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Wrap all content inside a div for styling container
st.markdown('<div class="main">', unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="title">✨ Semantyl ✨</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Your intelligent document question-answering assistant powered by Semantic Search and RAG. '
    'Upload your documents, ask questions, and get precise, grounded answers from your data. 🚀</p>',
    unsafe_allow_html=True,
)

# File uploader
uploaded_files = st.file_uploader(
    label='📂 Upload your files here (PDF, TXT, DOCX)',
    type=['pdf', 'txt', 'docx'],
    accept_multiple_files=True,
)

def get_file_ids(files):
    return [f.name + str(f.size) for f in files]

if uploaded_files:
    current_file_ids = get_file_ids(uploaded_files)
    previous_file_ids = st.session_state.get("file_ids")

    if current_file_ids != previous_file_ids:
        with st.spinner('⬆️ Processing your documents...'):
            files_as_text = read_files(uploaded_files)
            searcher = SemanticSearch(files_as_text)
            searcher.process_files()
            st.session_state.searcher = searcher
            st.session_state.file_ids = current_file_ids
        st.success("Documents processed successfully!")

# Query input
query = st.text_input('❓ Enter your query here...')

# Query handling and response
if query:
    if "searcher" not in st.session_state:
        st.warning("⚠️ Please upload documents before asking a question.")
    else:
        with st.spinner('🔍 Searching your documents...'):
            response = st.session_state.searcher.produce_output(query)
            st.markdown(f'<div class="response-box">{response}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
