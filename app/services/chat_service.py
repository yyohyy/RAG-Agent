import uuid
from langchain.agents import create_react_agent, AgentExecutor
from langchain.agents.react.output_parser import ReActOutputParser
from langchain import hub
from langchain_core.tools import Tool
from langchain_community.llms import Ollama
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_tavily import TavilySearch
from app.config.vector import search as qdrant_search
from app.config.redis import RedisMemory
from app.common.logger import get_logger
from app.common.variables import variables
from app.utils.constants import Constants

log = get_logger("ChatService")

class ChatService:
    def __init__(self):
        self.llm = Ollama(model="mistral", temperature=0.7) 
        self.web_tool = (
            TavilySearch(max_results=5)
            if variables.TAVILY_API_KEY else None
        )
        self._agent_cache = {}

    def build_agent(self, collection: str, session_id: str):
        key = (collection, session_id)
        if key in self._agent_cache:
            return self._agent_cache[key]

        def vector_tool(query: str) -> str:
            log.info(f"VectorSearch called with query: {query}")
            hits = qdrant_search(collection, query, k=4)
            return "\n\n".join(h.payload["text"] for h in hits)

        vector_search_tool = Tool(
            name="VectorSearch",
            func=vector_tool,
            description="Search relevant internal documents for a given query."
        )

        wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        wiki_tool.name = "wikipedia" 
        if self.web_tool:
            def tavily_tool(query: str) -> str:
                log.info(f"TavilyWeb called with query: {query}")
                results = self.web_tool.run(query)
                
                if isinstance(results, list):
                    return "\n".join(r.get("snippet", str(r)) for r in results)
                elif isinstance(results, dict):
                    return results.get("snippet", str(results))
                else:
                    return str(results)

        tavily_tool=Tool(
            name="Tavily",
            func=tavily_tool,
            description="Search the open web for recent information. Input: query string."
                )
#             
        tools = [vector_search_tool, wiki_tool, tavily_tool]

        base_prompt = hub.pull("langchain-ai/react-agent-template")

        prompt = base_prompt.partial(instructions=Constants.instructions)

        agent = create_react_agent(
            llm=self.llm,
            tools=tools,
            prompt=prompt
        )

        memory = RedisMemory(session_id=session_id)

        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=memory,
            verbose=True,
            output_parser=ReActOutputParser(), 
            handle_parsing_errors=True,
            max_iterations=5,
            return_intermediate_steps=True
        )

        self._agent_cache[key] = agent_executor
        return agent_executor

    def ask(self, question: str, collection: str, session_id: str | None = None) -> str:
        session_id = session_id or str(uuid.uuid4())
        agent = self.build_agent(collection, session_id)
        result = agent.invoke({"input": question})
        log.info("Session %s | Q: %s | A: %s", session_id, question, result)
        return result.get("output", "I could not find a suitable answer.")