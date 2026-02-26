import os
import pandas as pd
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# 1. Load Environment Variables
load_dotenv()

def ingest_data():
    # Path configuration
    RAW_DATA_PATH = "data/raw/"
    VECTOR_STORE_PATH = "data/vector_store/"
    
    print("🚀 Starting FREE data ingestion (HuggingFace + ChromaDB)...")

    # --- PART 1: PROCESS PDFs ---
    documents = []
    pdf_files = ["aio.pdf", "cfpb.pdf"]

    for pdf in pdf_files:
        path = os.path.join(RAW_DATA_PATH, pdf)
        if os.path.exists(path):
            print(f"📄 Loading {pdf}...")
            loader = PyPDFLoader(path)
            documents.extend(loader.load())
        else:
            print(f"⚠️ Warning: {pdf} not found in {RAW_DATA_PATH}")

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200
    )
 # Increased overlap)   
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} text chunks from PDFs.")

    # --- PART 2: PROCESS CSV SCHEMA ---
    csv_path = os.path.join(RAW_DATA_PATH, "creditcard.csv")
    if os.path.exists(csv_path):
        print("📊 Processing creditcard.csv schema...")
        df = pd.read_csv(csv_path, nrows=1) 
        csv_context = (
            f"Banking Fraud Dataset Info: The dataset 'creditcard.csv' contains transactions. "
            f"Columns include: {', '.join(df.columns)}. "
            f"The 'Class' column indicates fraud (1) or legitimate (0). "
            f"Features V1-V28 are PCA-transformed components for privacy."
        )
        chunks.append(Document(page_content=csv_context, metadata={"source": "csv_metadata"}))

    # --- PART 3: CREATE LOCAL VECTOR STORE ---
    print("🧠 Generating local embeddings (this may take a minute)...")
    # This model runs on your machine for free
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_STORE_PATH
    )
    
    print(f"✨ Success! Vector store saved at {VECTOR_STORE_PATH}")

if __name__ == "__main__":
    ingest_data()