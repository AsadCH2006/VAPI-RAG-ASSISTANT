from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
    FilterSelector,
)

from config.settings import (
    EMBEDDING_MODEL,
    GEMINI_API_KEY,
    QDRANT_API_KEY,
    QDRANT_COLLECTION,
    QDRANT_URL,
)


class QdrantService:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL,
            google_api_key=GEMINI_API_KEY,
        )

        self.client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )

        self._create_collection_if_not_exists()

        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=QDRANT_COLLECTION,
            embedding=self.embeddings,
        )

    def _create_collection_if_not_exists(self):
        collections = self.client.get_collections().collections
        exists = any(collection.name == QDRANT_COLLECTION for collection in collections)

        if exists:
            return

        vector_size = len(self.embeddings.embed_query("test"))

        self.client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

        self.client.create_payload_index(
            collection_name=QDRANT_COLLECTION,
            field_name="metadata.source",
            field_schema="keyword",
        )

    def add_documents(self, documents):
        self.vector_store.add_documents(documents)

    def get_retriever(self, k):
        return self.vector_store.as_retriever(
            search_kwargs={
                "k": k,
            }
        )

    def list_documents(self):
        summary = {}
        next_offset = None

        while True:
            points, next_offset = self.client.scroll(
                collection_name=QDRANT_COLLECTION,
                limit=200,
                offset=next_offset,
                with_payload=True,
                with_vectors=False,
            )

            for point in points:
                payload = point.payload or {}
                metadata = payload.get("metadata", {})
                filename = metadata.get("source", "unknown")

                if filename not in summary:
                    summary[filename] = 0
                summary[filename] += 1

            if next_offset is None:
                break

        return [
            {"filename": filename, "chunks": count}
            for filename, count in summary.items()
        ]

    def get_stats(self):
        info = self.client.get_collection(QDRANT_COLLECTION)
        documents = self.list_documents()

        return {
            "total_chunks": info.points_count,
            "total_documents": len(documents),
        }

    def delete_document(self, filename):
        self.client.delete(
            collection_name=QDRANT_COLLECTION,
            points_selector=FilterSelector(
                filter=Filter(
                    must=[
                        FieldCondition(
                            key="metadata.source",
                            match=MatchValue(value=filename),
                        )
                    ]
                )
            ),
        )
