# This is a service that implements some form of semantic search using embeddings/vectorDB
from app.schemas import ProductPreview


class SearchService:
    def __init__(self) -> None:
        # Placeholder for dependency injection (e.g. vector DB client)
        pass

    def semantic_search(self, query: str, top_k: int = 10) -> list[ProductPreview]:
        """
        Placeholder semantic search implementation.

        For now, returns an empty list so that the /semantic-search endpoint
        works without raising errors. Replace this with real vector search
        against your product catalog when ready.
        """
        _ = (query, top_k)  # prevent unused-variable warnings
        return []
