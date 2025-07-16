from fastapi import APIRouter, UploadFile, HTTPException, Form
from app.services.rag_service import RAGService
from app.services.chat_service import ChatService
from app.schemas.schema import ChatIn
import uuid
from app.common.variables import variables

router=APIRouter()
rag=RAGService()
chat_service = ChatService()

@router.post("/upload")
async def upload(file:UploadFile, collection:str=Form(variables.QDRANT_COLLECTION), chunker:str=Form("recursive"), embedder:str=Form("mini-lm")):
    ext=file.filename.split(".")[-1].lower()
    if ext not in("pdf","txt"): 
        raise HTTPException(415,"Only .pdf or .txt allowed")
    rag.ingest_file(await file.read(), file.filename, ext, collection, chunker, embedder) 
    return {"status": True, "message": f"File '{file.filename}' successfully loaded."}

@router.post("/chat")
def chat(payload: ChatIn):
    session_id = payload.session_id or str(uuid.uuid4())
    question = payload.question
    collection = variables.QDRANT_COLLECTION
    try:
        answer = chat_service.ask(
            question=question,
            collection=collection,
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(500, str(e))
    return {
        "session_id": session_id, 
        "answer": answer
    }