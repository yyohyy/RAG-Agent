# RAG Agent

## Tools Used

- Python 3.12
- FastAPI
- Pydantic / Pydantic Settings
- PostgreSQL
- Uvicorn
- Redis
- Qdrant
- Langchain
- Tvily

## How to Run the Application

1. Clone the repository[on Windows]:

   ```bash
   git clone https://github.com/yyohyy/12-Factor-Digit-Classifier.git
   cd 12-Factor-Digit-Classifier
   ```
   
2. Set .env file 

```
  POSTGRES_USER=youruser
  POSTGRES_PASSWORD=yourpassword
  POSTGRES_DB=yourdb
  POSTRGRES_URL=url
  REDIS_URL=redis://redis:6379
  QDRANT_URL=http://qdrant:6333
  OLLAMA_API=http://ollama:11434
  OLLAMA_EMBED_MODEL=your-embed-model
  OLLAMA_LLM_MODEL=your-llm-model
  TAVILY_API_KEY=your-tavily-key
  SMTP_HOST=smtp.gmail.com
  SMTP_PORT=465
  SMTP_USER=your-email@gmail.com
  SMTP_PASSWORD=your-app-password
```

3. Run services

```
  docker-compose up --build
```
