
import sys
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.gemini import GeminiEmbedding
from exception import customexception
from logger import logging

def download_gemini_embedding(model, document):
    try:
        logging.info("Initializing Gemini Embedding model...")
        
        gemini_embed_model = GeminiEmbedding(model_name="models/gemini-embedding-001")
        
        # Global assignments
        Settings.llm = model
        Settings.embed_model = gemini_embed_model
        Settings.chunk_size = 2000
        Settings.chunk_overlap = 100
        
        logging.info("Building VectorStoreIndex from documents...")
        index = VectorStoreIndex.from_documents(document)
        
        logging.info("Persisting storage index cache artifacts locally...")
        index.storage_context.persist(persist_dir="./storage")
        
        logging.info("Assembling query engine configuration pipeline...")
        query_engine = index.as_query_engine()
        return query_engine
        
    except Exception as e:
        raise customexception(e, sys)
