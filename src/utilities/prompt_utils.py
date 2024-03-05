from typing import List, AsyncGenerator

def generate_prompt(query: str, documents: List[dict]) -> AsyncGenerator[str, None]:
    document_texts = [doc['text_content'] for doc in documents if 'text_content' in doc]
    total_document_text = ". ".join(document_texts)

    prompt = f"Question: {query}. \n\n Create an answer from the following content as reranked documents in chunked form: {total_document_text}"

    return prompt