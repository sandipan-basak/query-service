import os
from dotenv import load_dotenv
import json

load_dotenv()

class MetadataService:
    def __init__(self, metadata_file_path):
        self.metadata = self.load_metadata(metadata_file_path)

    def load_metadata(self, file_path):
        with open(file_path, 'r') as f:
            metadata = json.load(f)
        return metadata

    def get_document_details_by_index(self, index):
        for item in self.metadata:
            if item["faiss_index"] == index:
                return item
        return None

def get_metadata_service():
    metadata_file_path = os.getenv('FAISS_METADATA_PATH', '/usr/src/app/data/indices/metadata.json')
    metadata_service = MetadataService(metadata_file_path)
    return metadata_service