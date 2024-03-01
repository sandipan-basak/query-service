from pydantic import BaseModel
from typing import List

class QueryList(BaseModel):
    queries: List[str]
