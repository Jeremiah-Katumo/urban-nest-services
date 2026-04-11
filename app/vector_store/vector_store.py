import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Cassandra, FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from .local_creds import (
    ASTRA_DB_API_ENDPOINT,
    ASTRA_DB_APPLICATION_TOKEN,
    ASTRA_DB_COLLECTION,
    ASTRA_DB_KEYSPACE,
)

load_dotenv()


class VectorStoreService:
    
    def __init__(self):
        self.embedding = OllamaEmbeddings() # OpenAIEmbeddings()
        self.vector_store = AstraDBVectorStore(
            collection_name=ASTRA_DB_COLLECTION,
            embedding=self.embedding,
            token=ASTRA_DB_APPLICATION_TOKEN,
            api_endpoint=ASTRA_DB_API_ENDPOINT
        )
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
    async def add_documents(self, docs: list):
        return self.vector_store.add_documents(docs)
    
    async def from_documents(self, docs: list):
        return self.vector_store.from_documents(docs, self.embedding)
        
    async def similarity_search(self, query: str, search_kwargs: int = 5):
        return self.vector_store.similarity_search(query, search_kwargs)
    
    async def retriever(self):
        return self.vector_store.as_retriever()
    
    async def split_text(self, docs: list):
        return self.text_splitter.split_documents(docs)
    
    async def retrieval_chain(self, retriever, document_chain):
        return create_retrieval_chain(retriever, document_chain)
        
    async def property_to_text(self, propertyy):
        return f"""
        Title: {propertyy.title}
        Location: {propertyy.location}
        Bedrooms: {propertyy.bedrooms}
        Price: {propertyy.price}
        Description: {propertyy.description}
        """
        
    async def index_properties(self, properties):
        docs = [await self.property_to_text(p) for p in properties]
        return self.vector_store.add_documents(docs)