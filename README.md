# My Chatbot

## Overview

My Chatbot is an AI-powered conversational agent designed to answer user queries based on PDF documents. The chatbot leverages LangChain, Google Generative AI, and FAISS to provide detailed answers by analyzing the content of uploaded PDF files. Users can also provide their contact information if they request a callback or further assistance.

## Features

- **PDF Processing**: Upload multiple PDF files, and the chatbot will extract and process the text for later querying.
- **Contextual Question Answering**: Ask questions related to the uploaded PDF files, and the chatbot will provide answers based on the content.
- **Contact Information Form**: Users can submit their contact information if they ask the chatbot to call them.
- **Powered by Google Generative AI**: Utilizes Google's Gemini model to generate accurate and detailed responses.

## How It Works

1. **PDF Upload**: Users can upload multiple PDF files via the sidebar.
2. **Text Extraction and Processing**: The text from the PDF files is extracted and split into manageable chunks for processing.
3. **Vector Store Creation**: A FAISS vector store is created from the text chunks, enabling efficient similarity search when answering questions.
4. **Question Answering**: Users can input questions, and the chatbot will search for relevant context within the processed PDFs to generate an answer.
5. **User Interaction**: If a user asks the chatbot to contact them, a form is presented to collect their name, phone number, and email address.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following:

- Python 3.8 or later
- A Google API key for accessing Google Generative AI services

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/smabid2018/My-Chatbot.git
   cd My-Chatbot
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   - Create a `.env` file in the root directory and add your Google API key:
     ```plaintext
     GOOGLE_API_KEY=your-google-api-key
     ```

### Usage

1. **Run the application**:

   ```bash
   streamlit run chatbot.py
   ```

2. **Upload PDF files**:

   - Use the sidebar to upload one or more PDF files.
   - Click the "Submit & Process" button to process the PDFs.

3. **Ask questions**:

   - Enter a question related to the content of the PDFs in the text input box.
   - If the question is related to contacting you (e.g., "call me"), the chatbot will ask for your contact information.

4. **View responses**:
   - The chatbot will provide detailed answers based on the content of the uploaded PDFs.

### Example

Here’s how to interact with the chatbot:

- **Upload PDFs**: Drag and drop PDF files into the sidebar uploader.
- **Ask a Question**: Type a question like "What is the main topic of the first document?".
- **Contact Request**: If you type "call me", the chatbot will prompt you to enter your contact details.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a clear description of your changes.
