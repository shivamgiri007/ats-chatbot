import weaviate
from app.config import settings
from app.models.weaviate.document import WeaviateDocument

class VectorDBController:
    def __init__(self):
        self.client = weaviate.Client(
            url=settings.weaviate_url,
            additional_headers={"X-OpenAI-Api-Key": settings.openai_api_key}
        )
        
    async def search_documents(self, query: str, k: int = 3) -> list[str]:
        try:
            result = self.client.query.get(
                "Document",
                ["content"]
            ).with_near_vector({
                "vector": []  # Need to add embedding vector here
            }).with_limit(k).do()
            
            return [item["content"] for item in result["data"]["Get"]["Document"]]
        except Exception as e:
            print(f"Vector search error: {e}")
            return []
