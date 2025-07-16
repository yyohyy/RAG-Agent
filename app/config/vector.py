import uuid
from functools import lru_cache
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from langchain_community.embeddings import OllamaEmbeddings
from app.common.logger import get_logger
from app.common.variables import variables

log = get_logger("Qdrant")

@lru_cache(maxsize=1)
def client() -> QdrantClient:
    return QdrantClient(url=variables.QDRANT_URL)

def ensure_collection(name: str, vector_size: int):
    qc = client()
    if name not in [c.name for c in qc.get_collections().collections]:
        qc.create_collection(
            collection_name=name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )
        log.info("Created Qdrant collection '%s'", name)


def upsert_docs(collection: str, docs: list[dict]):
    texts   = [d["text"] for d in docs]
    payload = [{"source": d["source"], "text": d["text"]} for d in docs]

    embedder = OllamaEmbeddings(model=variables.OLLAMA_EMBED_MODEL)
    vectors  = embedder.embed_documents(texts)

    ensure_collection(collection, vector_size=len(vectors[0]))

    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vec,
            payload=pl,
        )
        for vec, pl in zip(vectors, payload)
    ]
    client().upsert(collection_name=collection, points=points)
    log.info("Upserted %d vectors into '%s'", len(points), collection)

def search(collection: str, query: str, k: int = 4):
    embedder = OllamaEmbeddings(model=variables.OLLAMA_EMBED_MODEL)
    q_vec    = embedder.embed_query(query)
    hits = client().search(
        collection_name=collection,
        query_vector=q_vec,
        limit=k,
    )
    return hits  
