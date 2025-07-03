from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.chat_models import init_chat_model


class SemanticSearch:
	def __init__(self, files):
		self.files = files
		self.documents = []
		self.splits    = None
		self.db        = None
		self.hf_embed  = HuggingFaceEmbeddings(
			model_name="sentence-transformers/all-mpnet-base-v2",
			model_kwargs={"device":"cpu"}
		)
		self.process_files()
		self.llm       = init_chat_model("command-r-plus", model_provider="cohere")
		self.relevant_splits = []

	def create_documents(self):
		for file in self.files:
			self.documents.append(Document(
				page_content=file
			))

	def create_splits(self):
		text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
		self.splits   = text_splitter.split_documents(self.documents)

	def create_split_embeddings(self):
		self.db    = InMemoryVectorStore(embedding=self.hf_embed)		
		self.db.add_documents(documents=self.splits)

	def process_files(self):
		self.create_documents()
		self.create_splits()
		self.create_split_embeddings()

	def search_db(self, query):
		self.relevant_splits =  self.db.similarity_search(
			query=query,
			k=3
		)

	def produce_output(self, query):
		self.search_db(query)

		texts = '\n\n'.join([doc.page_content for doc in self.relevant_splits])
		messages = [
			SystemMessage(f"""
Here is the user query and relevant text chunks. 
Step 1: Summarize user question in simpler words. 
Step 2: Decide which retrieved text chunks directly apply. 
Step 3: Combine those chunks into an outline. 
Step 4: Draft a single, coherent answer. 
Show all steps, then provide a final refined answer.”


{texts}
"""),
			HumanMessage(query)
		]


		response = self.llm.invoke(messages)
		
		return response.content


	
