# app.py (updated with modern UI support)
from flask import Flask, request, render_template, flash
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages

UPLOAD_FOLDER = "14.AcedemyResearchAnalyzer\\uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        queryMain = request.form['prompt']

        if not uploaded_file or uploaded_file.filename == '':
            flash('No file selected', 'error')
            return render_template("upload.html")
            
        if not uploaded_file.filename.lower().endswith('.pdf'):
            flash('Please upload a PDF file', 'error')
            return render_template("upload.html")

        try:
            filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(filepath)

            # Process PDF
            loader = PyPDFLoader(filepath)
            docs = loader.load()
            texts = [doc.page_content for doc in docs]
            
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.create_documents(texts)

            embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
            
            # Initialize Chroma
            chroma_dir = "14.AcedemyResearchAnalyzer/my_chroma_db"
            collection_name = "sample"
            
            import chromadb
            client = chromadb.PersistentClient(path=chroma_dir)
            
            try:
                client.delete_collection(collection_name)
            except:
                pass
            
            vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=embedding,
                persist_directory=chroma_dir,
                collection_name=collection_name
            )

            retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

            prompt1 = PromptTemplate(
                template="""
                You are a helpful assistant.
                Answer in professional manner.
                If the context is insufficient, just say you don't know.

                {context}
                Question: {question}
                """,
                input_variables=["context", "question"],
            )

            def format_docs(retrieved_docs):
                return "\n\n".join(doc.page_content for doc in retrieved_docs)

            chain = (
                RunnableParallel({"context": retriever | format_docs, "question": RunnablePassthrough()})
                | prompt1
                | ChatGoogleGenerativeAI(model="models/gemini-1.5-flash")
                | StrOutputParser()
            )

            result = chain.invoke(queryMain)
            os.remove(filepath)
            
            return render_template("result.html", result=result, question=queryMain)
            
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return render_template("upload.html")

    return render_template("upload.html")

if __name__ == '__main__':
    app.run(debug=True)