# 📄 PDF Research Analyzer

An AI-powered web application that analyzes academic PDF files and answers user queries using Google Gemini via LangChain. The system leverages document embeddings and vector similarity to provide meaningful insights based on the uploaded content.

## 🚀 Features

- 🔍 Intelligent Q&A from academic PDFs
- 🧠 Uses Google Gemini AI via LangChain for context-aware answers
- 🧾 Semantic text chunking and storage with Chroma vector database
- 📤 Simple Flask-based UI for uploading PDFs and asking questions

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS3 (via Flask templates)
- **Backend:** Python, Flask
- **AI & NLP:** Google Generative AI (Gemini), LangChain
- **Embeddings:** GoogleGenerativeAIEmbeddings (`text-embedding-004`)
- **Vector Store:** ChromaDB
- **PDF Parsing:** PyPDFLoader (LangChain Community Loader)

## 📂 Directory Structure

```
  AcedemyResearchAnalyzer/
  │
  ├── uploads/ # Uploaded PDFs
  ├── my_chroma_db/ # Persistent Chroma vector store
  ├── templates/
  │ ├── upload.html # File upload and prompt form
  │ └── result.html # Output result page
  ├── app.py # Main Flask app
```


## 🧰 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pdf-research-analyzer.git
   cd pdf-research-analyzer

2. **Create a virtual environment and activate it**

3. **Install the dependencies**

4. ```bash
   pip install -r requirements.txt


5. **Run the file with:**
   ```bash
   python app.py
