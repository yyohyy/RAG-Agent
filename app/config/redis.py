from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.memory import ConversationBufferMemory
from app.common.variables import variables

class RedisMemory(ConversationBufferMemory):
    def __init__(self, session_id: str):
        history = RedisChatMessageHistory(
            url=variables.REDIS_URL,
            session_id=session_id,
            ttl= 7 * 24 * 60 * 60  
        )
        super().__init__(
            chat_memory=history,
            memory_key=variables.REDIS_MEMORY_KEY,
            return_messages=True
        )
