import cohere
from typing import List

co = cohere.Client('your-cohere-api-key')

def rerank(query: str, documents: List[str]) -> List[str]:
    response = co.rerank(
        model='medium',
        inputs=[{
            'query': query,
            'documents': documents
        }]
    )
    # Assuming the response includes reranked documents in the desired format
    return [doc.text for doc in response.reranked_inputs[0].documents]