from typing import List, Dict, Any

from intake import VectorStore, embedding_model
from langchain_community.embeddings import HuggingFaceEmbeddings
import os



class RAGRetriever:
    def __init__(self, vector_store, embedding_model):
        self.vector_store = vector_store
        self.embedding_model = embedding_model

    def retrieve(self, query: str, top_k: int = 5, score_threshold: float = 0.0) -> List[Dict[str, Any]]:
        print(f"Retrieving relevant documents for query: '{query}'")
        print(f"Top K: {top_k}, Score threshold: {score_threshold}")
        
        # Generate embedding
        embeddings = self.embedding_model.generate_embeddings([query])
        
        # FIXED: NumPy-safe check for empty or missing embeddings
        if embeddings is None or len(embeddings) == 0:
            print("Error: Embedding generation failed. Returned empty or None.")
            return []
            
        query_embedding = embeddings[0]  

        try:
            results = self.vector_store.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k,
                include=["metadatas", "documents", "embeddings", "distances"] 
            )
            
            retrieved_docs = []
            docs = results.get("documents")
            
            # Check if docs exist and are not empty
            if docs is not None and len(docs) > 0 and len(docs[0]) > 0:
                documents = docs[0]
                metadatas = results.get("metadatas", [[]])[0]
                distances = results.get("distances", [[]])[0]
                ids = results.get("ids", [[]])[0]
                
                for i, (doc, metadata, distance, doc_id) in enumerate(zip(documents, metadatas, distances, ids)):
                    if distance is None:
                        continue 
                        
                    similarity_score = 1 - distance 
                    
                    if similarity_score >= score_threshold:
                        retrieved_docs.append({
                            "id": doc_id,
                            "document": doc,
                            "metadata": metadata,
                            "distance": distance,
                            "content": doc,
                            "similarity_score": similarity_score,
                            "rank": i + 1
                        })
                print(f"Retrieved {len(retrieved_docs)} documents that meet the score threshold.")
            else:
                print("No documents retrieved from the vector store.")
                
            return retrieved_docs
            
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return []
if __name__ == "__main__":
    print("Starting the one-time data retrieval process...")
    
    # Create VectorStore instance
    vector_store_instance = VectorStore(
        collection_name="indian_court_cases", 
        persist_directory="../data/sc_judgments_db"
    )
    embedding_model_instance = embedding_model()
    
    # Create RAGRetriever with proper VectorStore instance
    retriever_instance = RAGRetriever(vector_store=vector_store_instance, embedding_model=embedding_model_instance)    
    
    # Call the retrieve method and store the results in a variable
    results = retriever_instance.retrieve(
            query="What are the established judicial guidelines and tests for a High Court or Sessions Court to grant anticipatory bail under Section 438 of the CrPC in cases involving complex economic offences or financial fraud? Specifically looking for cases that weigh the apprehension of the accused tampering with evidence or influencing witnesses against their right to personal liberty", 
            top_k=3, 
            score_threshold=0.2
        )

    # Print the results to see what you got
    print(results)
   
    # Initialize variables as None
#this below part is for this specific case/project

#     case1 = case2 = case3 = None

# # Assign based on what was actually found
#     if len(results) >= 1:
#         case1 = results[0]
#     if len(results) >= 2:
#         case2 = results[1]
#     if len(results) >= 3:
#         case3 = results[2]

# # Usage example:
#     if case1:
#         content_for_llm = case1["content"]
#         source_file = case1["id"]
#         print(f"Case 1 content: {content_for_llm}")
#         print(f"Case 1 source file: {source_file}") 