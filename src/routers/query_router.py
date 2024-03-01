from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List
from src.utilities.cohere_embeddings import query_to_embedding
from src.models.query_models import QueryList
import numpy as np
from src.utilities.faiss_utils import FAISSService, get_faiss_service
from src.utilities.metadata_utils import MetadataService, get_metadata_service
from src.utilities.rerank import rerank_documents_with_chunks
from src.utilities.semantic_cache import RedisSemanticCache, get_redis_semantic_cache
from src.utilities.openai import generate_response_from_documents


router = APIRouter()

@router.post("/query")
async def handle_query(
    query_list: QueryList, 
    faiss_service: FAISSService = Depends(get_faiss_service), 
    metadata_service: MetadataService = Depends(get_metadata_service),
    cache_service: RedisSemanticCache = Depends(get_redis_semantic_cache)
):
    try:
        query_responses: Dict[str, List[str]] = {}

        for query in query_list.queries:
            # Convert query to embedding
            query_embedding = np.array(query_to_embedding([query])[0])
            print(f"Initial query_embedding shape: {query_embedding.shape}")
            
            # cached_responses = cache_service.find_most_similar_response(query_embedding.copy())
            # print(f"Cache result found: {cached_responses}, query_embedding shape after cache check: {query_embedding.shape}")

            # if cached_responses:
            #     query_responses[query] = cached_responses
            # else:
            distances, indices = faiss_service.search(query_embedding.copy().reshape(1, -1), top_k=10)
            print(f"Query_embedding shape after FAISS search: {query_embedding.shape}")

            print("indices found")
            documents = [metadata_service.get_document_details_by_index(index) for index in indices.flatten()]
            print("documents details from metadata")

            reranked_documents = rerank_documents_with_chunks(query, documents)
            print("rerank_documents done")
            # Generate a response based on documents
            response = generate_response_from_documents(query, reranked_documents)
            print(f"response invoked : {response}")

            # Store new query and its response in the cache
            # cache_service.store_embedding(query_embedding.copy(), response)
            # print(f"Query_embedding shape after store_embedding: {query_embedding.shape}")

            # Store the newly generated response
            query_responses[query] = [response]

        return query_responses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")