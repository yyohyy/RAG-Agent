import uuid
from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, Tool
from langchain_tavily import TavilySearch
from langchain.agents import ZeroShotAgent
from langchain.callbacks.base import BaseCallbackHandler
from app.config.vector import search as qdrant_search
from app.common.logger import get_logger
from app.common.variables import variables
from app.config.redis import RedisMemory

log = get_logger("ChatService")

class ToolLoggerCallback(BaseCallbackHandler):
    def on_tool_start(self, serialized, input_str, **kwargs):
        log.info(f"[ToolLogger] Tool started: {serialized['name']} with input: {input_str}")

    def on_tool_end(self, output, **kwargs):
        log.info(f"[ToolLogger] Tool finished with output: {output}")


class ChatService:
    def __init__(self):
        self.llm = OllamaLLM(model=variables.OLLAMA_LLM_MODEL)
        self.web_tool = (
            TavilySearch(max_results=5)
            if variables.TAVILY_API_KEY else None
        )

        self._agent_cache: dict[tuple[str, str], object] = {}

    def build_agent(self, collection: str, session_id: str):
        key = (collection, session_id)
        if key in self._agent_cache:
            return self._agent_cache[key]

        def vector_tool(query: str) -> str:
            log.info(f"VectorSearch called with query: {query}")
            hits = qdrant_search(collection, query, k=4)
            return "\n\n".join(h.payload["text"] for h in hits)

        tools = [
            Tool(
                name="VectorSearch",
                func=vector_tool,
                description="Retrieve relevant document chunks from internal docs. Input: search query string."
            )
        ]

        if self.web_tool:
            def tavily_tool(query: str) -> str:
                log.info(f"TavilyWeb called with query: {query}")
                return "\n".join(r["snippet"] for r in self.web_tool.run(query))

            tools.append(
                Tool(
                    name="TavilyWeb",
                    func=tavily_tool,
                    description="Search the open web for recent information. Input: query string."
                )
            )
        memory = RedisMemory(session_id=session_id)

        prompt = ZeroShotAgent.create_prompt(
            tools,
            prefix="You are an agent that can use these tools.",
            suffix="Use the following format:\nQuestion: {input}\nThought: ...\nAction: <tool name>\nAction Input: <input>\nObservation: ...",
)

        agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            prompt=prompt,
            agent="zero-shot-react-description",
            memory=memory,
            verbose=True,
            handle_parsing_errors=True,
            loop_count=0,
            max_iterations=10,
            callbacks=[ToolLoggerCallback()]
        )
        self._agent_cache[key] = agent
        return agent

    def ask(self, question: str, collection: str, session_id: str | None = None) -> str:
        session_id = session_id or str(uuid.uuid4())
        agent  = self.build_agent(collection, session_id)
        answer = agent.invoke(question)
        log.info("Session %s | Q: %s | A: %s", session_id, question, answer)
        return answer