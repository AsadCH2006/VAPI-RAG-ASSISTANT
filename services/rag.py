from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_groq import ChatGroq

from config.settings import (
    GROQ_API_KEY,
    GROQ_MODEL,
    TOP_K,
)

from prompts.prompt import RAG_PROMPT
from services.qdrant import QdrantService


class RAGService:
    def __init__(self):
        self.qdrant = QdrantService()

        self.llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
            temperature=0,
        )

        self.retriever = self.qdrant.get_retriever(TOP_K)

        self.document_chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=RAG_PROMPT,
        )

        self.chain = create_retrieval_chain(
            retriever=self.retriever,
            combine_docs_chain=self.document_chain,
        )

    def ask(self, question: str):
        response = self.chain.invoke(
            {
                "input": question,
            }
        )

        return response.get(
            "answer",
            "Sorry, I couldn't generate a response.",
        )
