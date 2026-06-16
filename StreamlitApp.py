import os
import shutil
import stat
import streamlit as st
from dotenv import load_dotenv

# Force environment variables to initialize immediately
load_dotenv()

# Modern LlamaIndex architectural elements
from llama_index.core import Settings, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.gemini import Gemini
from llama_index.core.readers.base import Document

# Setup workspace directory coordinates
DATA_DIR = "./data"
STORAGE_DIR = "./storage"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(STORAGE_DIR, exist_ok=True)

def clean_directory(directory_path):
    """
    Safely sweeps away files on Windows architectures without triggering
    WinError 5 Access Denied crashes from OneDrive background processes.
    """
    if not os.path.exists(directory_path):
        return
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.chmod(file_path, stat.S_IWRITE)
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path, onerror=lambda func, path, exc: (
                    os.chmod(path, stat.S_IWRITE), func(path)
                ))
        except PermissionError:
            pass # Gracefully sidestep brief sync engine background locks

# Streamlit App UI Configurations
st.set_page_config("Context Retrieval QA System")
st.header("QA System using LlamaIndex & Google Gemini 🚀")

# 1. Provide an upload file drag-and-drop zone
uploaded_file = st.file_uploader("Drop your reference knowledge file here", type=["txt", "pdf"])

# 2. Allow user text prompts
user_question = st.text_input("Ask a question based on your document data:")

if st.button("Submit"):
    if uploaded_file and user_question:
        with st.spinner("Processing vectors..."):
            try:
                # -------------------------------------------------------------
                # STEP A: INSULATE DIRECTORY & WRITE FILE TO DISK
                # -------------------------------------------------------------
                clean_directory(STORAGE_DIR)
                clean_directory(DATA_DIR)
                
                # Drop uploaded bytes buffer cleanly into the data directory
                target_file_path = os.path.join(DATA_DIR, uploaded_file.name)
                with open(target_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # -------------------------------------------------------------
                # STEP B: INJECT GLOBAL CONFIG OVERRIDES (SHUTS DOWN 429 ERRORS)
                # -------------------------------------------------------------
                # 1. Initialize Gemini strictly as the final text generator model
                gemini_api_key = os.getenv("GOOGLE_API_KEY")
                Settings.llm = Gemini(model="models/gemini-2.5-flash", api_key=gemini_api_key)
                
                # 2. Initialize a local HuggingFace Embedding model for document indexing.
                # Runs locally on your machine CPU. 0 network calls = 0 rate limits.
                local_embeddings = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
                Settings.embed_model = local_embeddings
                
                Settings.chunk_size = 1024
                Settings.chunk_overlap = 40

                # -------------------------------------------------------------
                # STEP C: BUILD VECTOR HOOKS & PERSIST DATA
                # -------------------------------------------------------------
                # Lazy import internal data ingestion to match your target layout structures cleanly
                from llama_index.core import SimpleDirectoryReader
                
                # Ingest data directly from directory strings safely
                documents = SimpleDirectoryReader(DATA_DIR).load_data()
                
                # Vectorize chunks locally 
                index = VectorStoreIndex.from_documents(documents)
                index.storage_context.persist(persist_dir=STORAGE_DIR)

                # -------------------------------------------------------------
                # STEP D: FORMULATE AND EXECUTE RUNTIME SEARCHES
                # -------------------------------------------------------------
                query_engine = index.as_query_engine()
                response = query_engine.query(user_question)
                
                # Display results cleanly on screen
                st.subheader("💡 Results:")
                st.write(response.response)
                
            except Exception as e:
                st.error(f"An unexpected initialization tracking error occurred: {str(e)}")
    else:
        st.warning("Please verify that both a reference file and a question payload are submitted.")