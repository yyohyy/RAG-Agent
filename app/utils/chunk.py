from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.common.variables import variables 

def recursive(text:str):
    return RecursiveCharacterTextSplitter(chunk_size=variables.CHUNK_SIZE, chunk_overlap=100).split_text(text)

def custom(text:str):
    pass

CHUNKERS = {"recursive":recursive, 
            "custom":custom}