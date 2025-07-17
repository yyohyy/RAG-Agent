import tempfile, os
from langchain_community.document_loaders import PyPDFLoader,TextLoader
from app.common.logger import get_logger
from app.utils.chunk import CHUNKERS
from app.config.vector import upsert_docs
from app.config.database import SessionLocal
from app.models.document import DocumentMetaData
        
class RAGService:
    def __init__(self):
        self.log=get_logger("RAGService")

    def ingest_file(self, file_bytes:bytes, filename:str, extension:str, collection:str, chunker:str, embedder:str):
        text=self.extract(file_bytes, extension)
        docs=[{"content": chunk, 
               "source": filename} for chunk in CHUNKERS[chunker](text)]

        upsert_docs(collection, [{"text":d["content"],"source":d["source"]} for d in docs])

        with SessionLocal() as db:
            db.add(DocumentMetaData(file=filename,n_chunks=len(docs),chunker=chunker,embedder=embedder)); db.commit()
        self.log.info("Ingested %d chunks for %s",len(docs),filename)

    def extract(self,b:bytes,ext:str)->str:
        with tempfile.NamedTemporaryFile(delete=False,suffix=f".{ext}") as tmp:
            tmp.write(b); path=tmp.name
        try:
            loader = PyPDFLoader(path) if ext=="pdf" else TextLoader(path)
            pages=loader.load(); return "\n".join(p.page_content for p in pages)
        finally:
            os.remove(path)