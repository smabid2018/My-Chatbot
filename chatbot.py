import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks,  embedding=embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

    prompt = PromptTemplate(template=prompt_template,
                            input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    new_db = FAISS.load_local(
        "faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "question": user_question}, return_only_outputs=True)
    st.write("Reply: ", response["output_text"])


def collect_user_info():
    # Initialize the session state variables if they are not already initialized
    if "submitted" not in st.session_state:
        st.session_state["submitted"] = False
        st.session_state["user_info"] = {}

    # Display the form if it hasn't been submitted yet
    if not st.session_state.submitted:
        st.write("Please submit your information.")
        with st.form("user_info_form"):
            name = st.text_input("Name")
            phone = st.text_input("Phone Number")
            email = st.text_input("Email")
            submitted = st.form_submit_button("Submit")

            if submitted and name and phone and email:
                st.session_state.submitted = True  # Mark the form as submitted
                st.session_state.user_info = {
                    "name": name, "phone": phone, "email": email}
                st.success(
                    "We successfully recieved your Contact Information!")

    # Display the user info after form submission
    if st.session_state.submitted:
        st.write(
            f"Thank you, {st.session_state.user_info['name']}! We will contact you at {st.session_state.user_info['phone']} or {st.session_state.user_info['email']}.")

    return st.session_state.user_info if st.session_state.submitted else None


def main():
    st.set_page_config("My Chatbot")
    st.header("Chat with PDF")
    st.text("Powered BY Gemini")
    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        if user_question.lower() in ["call me", "contact me", "reach me"]:
            collect_user_info()
        else:
            user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader(
            "Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")


if __name__ == "__main__":
    main()
