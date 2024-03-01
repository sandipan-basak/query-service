from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List

client = OpenAI(api_key=os.getenv('OPEN_API_KEY'))


load_dotenv()

def generate_response_from_documents(query, documents: List[dict]) -> str:
    # Combine the document summaries into a prompt for OpenAI
    document_texts = []

    for doc in documents:
        if isinstance(doc, dict) and 'text_content' in doc:
            document_texts.append(doc['text_content'])
        # else:
        #     print(f"Warning: Skipping document due to unexpected format or missing 'text_content' key: {doc}")
            
    total_document_text = "\n\n".join(document_texts)

    prompt = f"Get a summarised answer from the following content based on the query: {query}.. \n\n content as follows: {total_document_text}"

    # Call OpenAI API to generate a response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
    )

    if response.choices and response.choices[0].message:
        return response.choices[0].message.content.strip()
    else:
        return "No response generated."

