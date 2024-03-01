import redis
import os
import numpy as np
import hashlib
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()

class RedisSemanticCache:
    def __init__(self, redis_url):
        self.db = redis.Redis.from_url(redis_url)

    def generate_key_for_embedding(self, query_embedding):
        # Create a hash of the embedding for deterministic key generation
        hasher = hashlib.sha256()
        hasher.update(query_embedding.tobytes())
        return hasher.hexdigest()

    def store_embedding(self, query_embedding, response):
        key = self.generate_key_for_embedding(query_embedding)
        embedding_bytes = query_embedding.tobytes()
        print(f'query_embedding: {query_embedding}')
        print(f'embedding_bytes: {embedding_bytes}')
        actual_elements = len(embedding_bytes) // np.dtype(np.float32).itemsize
        print(f'np.dtype(np.float32): {np.dtype(np.float32)}')
        print(f'len(embedding_bytes): {len(embedding_bytes)}')
        print(f'actual_elements: {actual_elements}')
        shape_str = str(actual_elements)
        print(f'shape_str: {shape_str}')
        # byte_length = len(embedding_bytes)
        # Use the original embedding shape for storage, ensuring it's suitable for retrieval and use
        # shape_str = ','.join(map(str, [query_embedding.size]))

        print(f"[Store Embedding] Key: {key}, Shape: {shape_str},")
        self.db.set(f"embedding:{key}", embedding_bytes)
        self.db.set(f"shape:{key}", shape_str)  # Store shape accurately reflecting embedding's dimensions
        self.db.set(f"response:{key}", response)

    def find_most_similar_response(self, query_embedding, threshold=0.85):
        most_similar_response = None
        highest_similarity = threshold
        print(f"Finding most similar response for query_embedding shape: {query_embedding.shape}")
        query_embedding = query_embedding.reshape(1, -1) if query_embedding.ndim == 1 else query_embedding.copy()
        print(f'[Cache Check] Query Embedding Shape: {query_embedding.shape}')

        for key in self.db.scan_iter(match="embedding:*"):
            if not key.decode().startswith("embedding:"):
                continue
            
            shape_key = key.decode().replace("embedding:", "shape:")
            print(f'key.decode(): {key.decode()}')
            print(f'shape_key: {shape_key}')
            shape_str = self.db.get(shape_key).decode()
            print(f'shape_str: {shape_str}')
            # stored_shape = tuple(map(int, shape_str.split(',')))
            # print(f'stored_shape: {stored_shape}')

            stored_shape = (int(shape_str),)  # Accurately reconstruct the shape
            print(f'stored_shape: {stored_shape}')

            stored_embedding_bytes = self.db.get(key)
            
            try:
                # Reshape according to the stored shape
                if len(stored_shape) == 1 and stored_shape[0] > 1:  # 1D array with more than one element
                    stored_embedding = np.frombuffer(stored_embedding_bytes, dtype=np.float32).reshape(1, -1)
                    print(f'stored_embedding: {stored_embedding}')
                else:
                    stored_embedding = np.frombuffer(stored_embedding_bytes, dtype=np.float32).reshape(stored_shape)
                    print(f'stored_embedding: {stored_embedding}')

            except ValueError as e:
                print(f"[Error] Cannot reshape bytes to {stored_shape}: {e}")
                continue
            
            similarity = cosine_similarity(query_embedding, stored_embedding)[0][0]
            if similarity > highest_similarity:
                response_key = key.decode().replace("embedding:", "response:")
                most_similar_response = self.db.get(response_key).decode()
                highest_similarity = similarity

        return most_similar_response


def get_redis_semantic_cache() -> RedisSemanticCache:
    redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')
    cache = RedisSemanticCache(redis_url=redis_url)
    return cache

def parse_shape(shape_str):
    # Convert the shape string back into a tuple of integers
    return tuple(map(int, shape_str.split(',')))