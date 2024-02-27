from functools import lru_cache
from typing import List

@lru_cache(maxsize=100)  # Adjust maxsize as needed
def cached_rerank(query: str, documents: tuple) -> List[str]:
    # This function will wrap the rerank call and be cached
    # Convert documents from tuple back to list for the rerank function
    from cohere_rerank import rerank  # Import here to avoid circular dependency
    return rerank(query, list(documents))