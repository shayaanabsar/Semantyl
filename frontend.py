import streamlit as st
from file_converter import *
from backend import *
import re

st.set_page_config(
	page_title="Semantyl",
	page_icon="✨",
)

st.title('✨ Semantyl ✨')
st.write("""
Welcome to **Semantyl** — your intelligent document question-answering assistant powered by Semantic Search and Retrieval-Augmented Generation (RAG).  
Upload your documents, ask questions, and get precise, grounded answers from your own data. 🚀
""")

uploaded_files = st.file_uploader(
	label='📂 Upload your files here (PDF, TXT, DOCX) for querying',
	type=['pdf', 'txt', 'docx'],
	accept_multiple_files=True
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

query = st.text_input('❓ Enter your query here...')

if query:
	if "searcher" not in st.session_state:
		st.warning("⚠️ Please upload one or more documents before submitting a query.")
	else:
		with st.spinner('🔍 Searching your documents, please wait...'):
			response = st.session_state.searcher.produce_output(query)

			optimized_q = re.search(r"Optimized Question:\s*(.*)", response)
			passages    = re.search(r"Relevant Passages:\s*(.*)", response)
			answer      = re.search(r"Answer:\s*(.*)", response)

			if optimized_q:
				with st.expander("📝 Optimized Question"): st.markdown(optimized_q.group(1).strip())
			if passages:
				with st.expander("📚 Relevant Passages"): st.markdown(passages.group(1).strip())
			if answer:
				answer = answer.group(1).strip()
				if "do not contain enough information" in answer.lower() or "no relevant" in answer.lower():
					st.markdown("### ⚠️ No Answer Found")
					st.info(answer)
				else:
					st.markdown("### ✅ Final Answer")
					st.success(answer)
