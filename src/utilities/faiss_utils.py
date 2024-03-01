import faiss
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()

class FAISSService:
    def __init__(self, index_file_path):
        self.index = self.load_index(index_file_path)

    def load_index(self, file_path):
        if os.path.exists(file_path):
            return faiss.read_index(file_path)
        else:
            raise FileNotFoundError(f"FAISS index file not found at {file_path}")

    def search(self, query_embeddings, top_k):
        if not isinstance(query_embeddings, np.ndarray):
            query_embeddings = np.array(query_embeddings)

        if query_embeddings.ndim == 1:
            query_embeddings = query_embeddings.reshape(1, -1)
        elif query_embeddings.ndim == 2 and query_embeddings.shape[0] != 1:
            pass
        elif query_embeddings.ndim != 2:
            raise ValueError("Unsupported shape for query_embeddings.")
        

        # Check dimensionality consistency
        if query_embeddings.shape[1] != self.index.d:
            raise ValueError(f"Query embeddings dimension {query_embeddings.shape[1]} does not match index dimension {self.index.d}.")


        try:
            distances, indices = self.index.search(query_embeddings, top_k)
        except Exception as e:
            raise  # Optionally re-raise the exception or handle it accordingly
        return distances, indices
    
def get_faiss_service():
    index_file_path = index_file_path = os.getenv('FAISS_INDEX_PATH', '/usr/src/app/data/indices/combined_index.index')
    faiss_service = FAISSService(index_file_path)
    return faiss_service
