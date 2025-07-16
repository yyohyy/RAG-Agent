from langchain.embeddings import HuggingFaceEmbeddings

def get_embedder(name: str):
        model_map = {
            "mini-lm": "sentence-transformers/all-MiniLM-L6-v2",
        }
        model_name = model_map.get(name, "sentence-transformers/all-MiniLM-L6-v2")
        return HuggingFaceEmbeddings(model_name=model_name, model_kwargs={"device": "cpu"})