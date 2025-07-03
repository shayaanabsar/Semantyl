import PyPDF2
import docx
import streamlit as st

FILE_TYPES = {
	"application/pdf" : "PDF",
	"text/plain"      : "TXT",
	"application/vnd.openxmlformats-officedocument.wordprocessingml.document": "DOCX"
}

def read_pdf(file):
	reader = PyPDF2.PdfReader(file)

	text = ''

	for page in reader.pages:
		text += page.extract_text() + '\n'

	return text

def read_docx(file):
	doc = docx.Document(file)
	full_text = [para.text for para in doc.paragraphs]
	return "\n".join(full_text)


def read_files(files):
	files_as_text = []

	for file in files:
		file_type = FILE_TYPES[file.type]

		try:
			if file_type == 'PDF'  : files_as_text.append(read_pdf(file))
			if file_type == 'TXT'  : files_as_text.append(file.read().decode('UTF-8'))
			if file_type == 'DOCX' : files_as_text.append(read_docx(file))
		except:
			error = f'An error occured whilst reading file: {file}'
			st.text(error)

	return files_as_text



