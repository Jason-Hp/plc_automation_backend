# This is a service that implements some form of semantic search using embeddings/vectorDB and perhaps also RAGs & LLMs
from app.schemas import ProductPreview

class SearchService:
    def __init__(self):
        pass

    def semantic_search(self, query: str, top_k: int = 10) -> list[ProductPreview]:
        #TODO: implement semantic search logic here
        # Basically, convert the query to an embedding, search the vector DB for top_k similar items, and return them
        # Query is an actual query, for example "Find me products to automate a conveyor belt system", this 
        # search will return relevant products

        pass
