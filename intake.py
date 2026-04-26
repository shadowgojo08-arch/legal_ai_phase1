from langchain_community.document_loaders.csv_loader import CSVLoader
import csv as csv_module
from langchain_text_splitters import RecursiveCharacterTextSplitter
import numpy as np
from sentence_transformers import SentenceTransformer#embedding model is inside sentence_transformers library
import chromadb
from chromadb.config import Settings
import uuid
from typing import List, Dict, Any, Tuple
from sklearn.metrics.pairwise import cosine_similarity
import os
from langchain_community.document_loaders import  PyMuPDFLoader 
from langchain_community.document_loaders import UnstructuredExcelLoader
import os
class pdf_loader:
    
    def pdf_reader(file_path):
        directory_loader = PyMuPDFLoader(file_path)
        pdf_data = directory_loader.load()
        return pdf_data

    

    




class CSV_DataLoader:
    def __init__(self):
        # check size limit next time you face error while retrieval
        # Set size limit for CSV field
        csv_module.field_size_limit(int(1e9))
        loader = CSVLoader(file_path="data\pair_dataset.csv",encoding="utf-8")
        self.data = loader.load()

class Chunking:
    def split_doc(self, documents, chunk_size=1000, chunk_overlap=200):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        split_docs = text_splitter.split_documents(documents)

        if split_docs:
            # print(f"Content: {split_docs[0].page_content[:200]}...")
            print(f"Metadata: {split_docs[0].metadata}")
            print(f"Total number of chunks created: {len(split_docs)}")
        
            return split_docs


    
class embedding_model:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.load_model()

    def load_model(self):
        try:
            print(f"Loading model: {self.model_name} ")
            # TWEAK 1: Add device="cuda" here to force it onto your RTX 4050 
            # gemini suggested this to increase speed by using full gpu power
            # that did not worked and require to install 2.5 gb library or something will do that later if required
            self.model = SentenceTransformer(self.model_name) 
            print(f"Model loaded successfully. Embedding dimension: {self.model.get_sentence_embedding_dimension()}")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
            raise
            
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        if self.model is None:
            raise ValueError("Model not loaded. Cannot generate embeddings.")
        try:
            print(f"Generating embeddings for {len(texts)} texts...")
            # TWEAK 2: Add batch_size=256 here! This is the Speed Hack.
            embeddings = self.model.encode(texts, show_progress_bar=True, batch_size=256)
            print(f"Embeddings generated successfully. Shape: {embeddings.shape}")
            return embeddings
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise

class VectorStore:
    def __init__(self, collection_name: str = "indian_court_cases", persist_directory: str = "../data/sc_judgments_db"):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None
        self.initialize_vector_store()
    def initialize_vector_store(self):
        try:
            os.makedirs(self.persist_directory, exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            self.collection = self.client.get_or_create_collection(name=self.collection_name, metadata={"description": "Collection for document embeddings  and metadata "})
            print(f"Vector store initialized successfully at {self.persist_directory} with collection name '{self.collection_name}'")
            print(f"Existing documents in collection:{self.collection.count()}")  # Print the number of existing documents in the collection
        
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            raise
    def add_documents(self, documents: List[Any], embeddings: np.ndarray):
        if len(documents) != len(embeddings):
            raise ValueError("The number of documents and embeddings must be the same.")
        ids = []
        metadatas = []
        documents_texts = []
        embeddings_list = []
        #uuid method may not stop  repeating output so check it out later and update it
        for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
            doc_id = str(uuid.uuid4())
            ids.append(doc_id)
            #preparing meta data
            metadata = {
                "case_index": doc.metadata.get("case_index", -1),
                "summary": doc.metadata.get("summary", "No summary available"),
                "chunk_index": i
            }
            metadatas.append(metadata)
            documents_texts.append(doc.page_content)
            embeddings_list.append(embedding.tolist())  # Convert numpy array to list for JSON serialization
        # Replace your single self.collection.add() with this batching loop:
        try:
            batch_size = 1000
            for i in range(0, len(ids), batch_size):
                # Slice the lists into smaller chunks of 1000
                self.collection.add(
                    ids=ids[i : i + batch_size],
                    metadatas=metadatas[i : i + batch_size],
                    documents=documents_texts[i : i + batch_size],
                    embeddings=embeddings_list[i : i + batch_size]
                )
                print(f"Batch inserted: {i} to {i + batch_size}")
                
            print(f"Total documents in collection: {self.collection.count()}")
            
        except Exception as e:
            print(f"Error adding documents to vector store: {e}")
            raise

if __name__ == "__main__":
    print("Starting the one-time data ingestion process...")
    
    # 1. Load the data
    loader = CSV_DataLoader()
    
    # 2. Chunk the data
    chunker = Chunking()
    chunks = chunker.split_doc(loader.data)
    
    # 3. Setup models and database
    embedding_model_instance = embedding_model()
    vector_store_instance = VectorStore()
    
    # 4. Generate embeddings and add to database
    texts = [chunk.page_content for chunk in chunks]
    embeddings = embedding_model_instance.generate_embeddings(texts)
    vector_store_instance.add_documents(chunks, embeddings)
    
    print("Ingestion complete!")

