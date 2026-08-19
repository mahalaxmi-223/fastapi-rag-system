from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)


class VectorStoreService:

    COLLECTION_NAME = "documents"

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
    ):
        self.client = QdrantClient(
            host=host,
            port=port,
        )

    def create_collection(self):
        """
        Create the document collection if it does not already exist.
        """

        collections = self.client.get_collections()

        existing_collections = [
            collection.name
            for collection in collections.collections
        ]

        if self.COLLECTION_NAME not in existing_collections:

            self.client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE,
                ),
            )

    def collection_exists(self) -> bool:
        collections = self.client.get_collections()

        return any(
            collection.name == self.COLLECTION_NAME
            for collection in collections.collections
        )

    def add_chunks(
        self,
        chunks,
        embeddings: list[list[float]],
        document_id: str,
    ):
        """
        Store chunk embeddings and metadata in Qdrant.
        """

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks must match number of embeddings."
            )

        points = []

        for chunk, embedding in zip(chunks, embeddings):

            point = PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload={
                    "document_id": document_id,
                    "chunk_id": chunk.id,
                    "text": chunk.text,
                    "start_index": chunk.start_index,
                    "end_index": chunk.end_index,
                },
            )

            points.append(point)

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=points,
        )

        return len(points)