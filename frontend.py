import streamlit as st
from file_converter import *
from backend import *

# Page config with wider layout for a cleaner look
st.set_page_config(
    page_title="✨ Semantyl",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling enhancements
st.markdown("""
<style>
    /* Title styling */
    .title {
        font-size: 3.2rem;
        font-weight: 900;
        color: #7f00ff;
        text-align: center;
        margin-bottom: 0;
    }
    /* Subtitle paragraph styling */
    .subtitle {
        font-size: 1.3rem;
        font-weight: 500;
        color: #4a4a4a;
        text-align: center;
        margin-top: 0.2rem;
        margin-bottom: 2rem;
    }
    /* Custom button style */
    div.stButton > button {
        background: linear-gradient(90deg, #7f00ff, #e100ff);
        color: white;
        font-weight: bold;
        padding: 0.6rem 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(127, 0, 255, 0.3);
        transition: background 0.3s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #e100ff, #7f00ff);
        box-shadow: 0 6px 20px rgba(225, 0, 255, 0.6);
    }
    /* File uploader style */
    .stFileUploader > label {
        font-weight: 700;
        font-size: 1.1rem;
        color: #7f00ff;
    }
    /* Input box customization */
    div.stTextInput > label {
        font-weight: 700;
        color: #7f00ff;
        font-size: 1.1rem;
    }
    /* Response markdown styling */
    .response {
        background-color: #f8f1ff;
        padding: 1rem 1.5rem;
        border-radius: 15px;
        box-shadow: 0 0 10px #d7bfff;
        font-size: 1.05rem;
        line-height: 1.5;
        white-space: pre-wrap;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Page Header
st.markdown('<h1 class="title">✨ Semantyl ✨</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Welcome to <strong>Semantyl</strong> — your intelligent document question-answering assistant powered by Semantic Search and Retrieval-Augmented Generation (RAG).<br>Upload your documents, ask questions, and get precise, grounded answers from your own data. 🚀</p>',
    unsafe_allow_html=True
)

# Sidebar with instructions and info
with st.sidebar:
    st.header("📖 How to use Semantyl")
    st.markdown("""
    1. Upload your documents (PDF, TXT, DOCX).  
    2. Wait for processing to complete.  
    3. Enter your question in the input box.  
    4. Get instant, grounded answers from your data!
    """)
    st.markdown("---")
    st.markdown("**Tip:** Upload multiple files to expand your knowledge base!")

# File uploader with wide layout
uploaded_files = st.file_uploader(
    label='📂 Upload your files here (PDF, TXT, DOCX) for querying',
    type=['pdf', 'txt', 'docx'],
    accept_multiple_files=True,
    key="file_uploader"
)

def get_file_ids(files):
    return [f.name + str(f.size) for f in files]

if uploaded_files:
    current_file_ids = get_file_ids(uploaded_files)
    previous_file_ids = st.session_state.get("file_ids")

    if current_file_ids != previous_file_ids:
        with st.spinner('⬆️ Processing your documents, please wait...'):
            files_as_text = read_files(uploaded_files)
            searcher = SemanticSearch(files_as_text)
            searcher.process_files()
            st.session_state.searcher = searcher
            st.session_state.file_ids = current_file_ids
        st.success("✅ Documents processed successfully!")

# Query input with placeholder and submit button side-by-side
query_col, submit_col = st.columns([4,1])

with query_col:
    query = st.text_input('❓ Enter your query here...', placeholder="Ask anything about your documents...")

with submit_col:
    submit = st.button("Ask")

if submit:
    if not query.strip():
        st.warning("⚠️ Please enter a question before submitting.")
    elif "searcher" not in st.session_state:
        st.warning("⚠️ Please upload one or more documents before submitting a query.")
    else:
        with st.spinner('🔍 Searching your documents, please wait...'):
            response = st.session_state.searcher.produce_output(query)
            st.markdown(f'<div class="response">{response}</div>', unsafe_allow_html=True)
