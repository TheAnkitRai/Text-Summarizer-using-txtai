"""
Application that builds a summary of an input given by the user in the form of text or document.

"""


import streamlit as st
from txtai.pipeline import Summary, Textractor
from PyPDF2 import PdfReader

st.set_page_config(layout="wide")

# function for summarizing the text 
@st.cache_resource
def text_summary(text, maxlength=None):
    #create summary instance
    summary = Summary()
    text = (text)
    result = summary(text)
    return result

# function to extract the text from the pdf file
# Using PdfReader from the imported PyPDF2
def extract_text_from_pdf(file_path):
    # Open the PDF file using PyPDF2
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        page = reader.pages[0]
        text = page.extract_text()
    return text

# choice for the kind of input user want to give
choice = st.sidebar.selectbox("Select your choice", ["Summarize Text", "Summarize Document"])


# if the choice selected is for text input
if choice == "Summarize Text":
    st.subheader("Summarize Text")
    
    # Taking the input from the user
    input_text = st.text_area("Enter your text here")
    if input_text is not None:
        if st.button("Summarize Text"):
            col1, col2 = st.columns([1,1])
            with col1:
                st.markdown("**Your Input Text**")
                st.info(input_text)
            with col2:
                st.markdown("**Summary Result**")
                result = text_summary(input_text)
                st.success(result)

# if the choice selected is for document input
elif choice == "Summarize Document":
    st.subheader("Summarize Document")
    
    # Taking the document input from the user
    input_file = st.file_uploader("Upload your document here", type=['pdf'])
    if input_file is not None:
        if st.button("Summarize Document"):
            with open("doc_file.pdf", "wb") as f:
                f.write(input_file.getbuffer())
            col1, col2 = st.columns([1,1])
            # col1 for the extracted text
            with col1:
                st.info("File uploaded successfully")
                
                # Extracting text from the input and displaying it in col1
                extracted_text = extract_text_from_pdf("doc_file.pdf")
                st.markdown("**Extracted Text is Below:**")
                st.info(extracted_text)
            
            # col2 for the summary generated
            with col2:
                # extracting text from the input and then displaying its summary in col2
                st.markdown("**Summary Result**")
                text = extract_text_from_pdf("doc_file.pdf")
                doc_summary = text_summary(text)
                st.success(doc_summary)
                
