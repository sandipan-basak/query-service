from typing import List, AsyncGenerator

def generate_prompt(query: str, documents: List[dict]) -> AsyncGenerator[str, None]:
    document_texts = [doc['text_content'] for doc in documents if 'text_content' in doc]
    total_document_text = "\n\n".join(document_texts)

    prompt = f"Get a summarised answer from the following content based on the query: '{query}'. Content as follows: {total_document_text}"

    return prompt