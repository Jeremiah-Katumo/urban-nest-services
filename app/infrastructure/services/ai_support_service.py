from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
import json
from ...redis.redis_client import redis_client
from ...vector_store.vector_store import VectorStoreService


class AISupportService:

    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.3)
    
    async def get_memory(self, session_id: str):
        data = redis_client.get(session_id)
        return json.loads(data) if data else []

    async def save_memory(self, session_id: str, memory):
        redis_client.set(session_id, json.dumps(memory), ex=3600)

    async def build_prompt(self, role, query, history):
        return f"""
        User Role: {role}
        Previous Interactions: {history}

        Query: {query}

        Instructions:
        - Tenant → booking, searching property
        - Landlord → listing, payments insights
        - Agent → management operations
        - Answer using FAQs, policies, lease docs
        """

    async def ask(self, session_id: str, role: str, query: str):
        history = await self.get_memory(session_id)

        prompt = await self.build_prompt(role, query, history)

        response = self.llm.invoke(prompt).content

        history.append({"query": query, "response": response})
        await self.save_memory(session_id, history)

        return response


class AISupportServiceAdvanced:

    def __init__(self):
        self.llm = ChatOllama(temperature=0.2)
        self.vector = VectorStoreService()

    async def pre_guardrail(self, query: str):
        blocked = ["hack", "exploit"]
        if any(word in query.lower() for word in blocked):
            raise AttributeError("Unsafe query detected")
        return query

    async def post_guardrail(self, response: str):
        if "illegal" in response.lower():
            return "Response blocked due to unsafe content."
        return response

    async def get_memory(self, session_id):
        data = redis_client.get(session_id)
        return json.loads(data) if data else []

    async def save_memory(self, session_id, memory):
        redis_client.set(session_id, json.dumps(memory), ex=3600)

    async def embed(self, text: str):
        return self.vector.embedding.embed_query(text)

    async def get_search_results(self, query: str):
        return self.vector.similarity_search(query)

    async def get_possible_recommended_properties(self, query: str):
        results = await self.get_search_results(query)
        return [doc.page_content for doc in results]

    async def get_recommended_properties(self, query: str):
        docs = await self.get_possible_recommended_properties(query)

        prompt = f"""
        Based on the query: {query}
        Recommend best matching properties from:
        {docs}
        """

        return self.llm.predict(prompt)

    async def build_full_prompt(self, role, query, history, docs):
        return f"""
        ROLE: {role}

        CHAT HISTORY:
        {history}

        USER QUERY:
        {query}

        RETRIEVED CONTEXT:
        {docs}

        INSTRUCTIONS:
        - Tenant → booking, property search
        - Landlord → payments, listings
        - Agent → management insights
        - Use context strictly
        - Recommend properties if relevant
        """

    async def ask(self, session_id: str, role: str, query: str):
        # 🔒 Pre-guard
        query = await self.pre_guardrail(query)

        history = await self.get_memory(session_id)
        docs = await self.get_search_results(query)

        full_prompt = await self.build_full_prompt(role, query, history, docs)

        response = self.llm.predict(full_prompt)

        # 🔒 Post-guard
        response = await self.post_guardrail(response)

        # 💾 Save memory
        history.append({"q": query, "a": response})
        await self.save_memory(session_id, history)

        return response