import cohere
from dotenv import load_dotenv
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Assuming cohere client initialization as before
load_dotenv()
co = cohere.Client(os.getenv('COHERE_API_KEY'))

def rerank_documents_with_chunks(query, documents):
    texts_and_metadata = []
    for doc in documents:
        with open(doc['chunk_path'], 'r', encoding='utf-8') as file:
            text_content = file.read()
            texts_and_metadata.append({
                **doc,
                'text_content': text_content
            })

    texts = [item['text_content'] for item in texts_and_metadata]
    embeddings = co.embed(model='embed-english-light-v2.0', texts=[query] + texts).embeddings

    query_embedding = np.array(embeddings[0])
    doc_embeddings = np.array(embeddings[1:])

    similarities = cosine_similarity([query_embedding], doc_embeddings)[0]
    ranked_indices = np.argsort(similarities)[::-1]

    # Store reranked documents with their text content in the result
    reranked_documents = [texts_and_metadata[i] for i in ranked_indices]

    return reranked_documents