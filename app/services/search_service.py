from app.schemas import ProductPreview, Manufacturer
from openai import OpenAI
import tiktoken
from supabase import Client, create_client
import re
import os


class SearchService:
    def __init__(self) -> None:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=openai_api_key)
        self.embedding_model = "text-embedding-3-small"
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
        pass

    def _get_token_chunks(self, text: str, chunk_size: int=500, overlap: int=50) -> list[str]:
        tokens = self.tokenizer.encode(text)
        chunks = []
        for i in range(0, len(tokens), chunk_size - overlap):
            chunk_tokens = tokens[i:i + chunk_size]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
        
        return chunks
    
    def _get_embedding(self, text: list[str]) -> list[float]:
        return self.client.embeddings.create(input=text, model=self.embedding_model).data[0].embedding

    def _vector_search(self, query_embedding: list[float], top_k: int=10):
        response = self.supabase.rpc(
            'match_embeddings',
            {
                'query_embedding': query_embedding,
                'match_threshold': 0.79,
                'match_count': top_k
            }
        ).execute()

        return response.data
        

    def semantic_search(self, query: str, top_k: int = 10) -> list[ProductPreview]:
        """
        Perform semantic search using query embeddings.
        """
        query_embedding = self._get_embedding([query])
        results = self._vector_search(query_embedding, top_k)

        product_previews = []
        for result in results:
            manufacturer = Manufacturer(
                id=result.get("manufacturer_id"),
                name=result.get("manufacturer_name", "Unknown")
            )
            product = ProductPreview(
                id=result.get("id"),
                name=result.get("name"),
                part_number=result.get("part_number"),
                manufacturer=manufacturer,
                image_url=result.get("image_url")
            )
            product_previews.append(product)

        return product_previews
