import cohere
from dotenv import load_dotenv
import os

load_dotenv()
co = cohere.Client(os.getenv('COHERE_API_KEY'))


def query_to_embedding(queries: list[str]):
    response = co.embed(texts=queries, model='embed-english-light-v2.0')
    embeddings = response.embeddings
    return embeddings