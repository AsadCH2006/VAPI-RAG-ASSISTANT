from langchain_core.prompts import ChatPromptTemplate

RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI assistant.

Answer the user's question only using the provided context.

If the answer cannot be found in the context, respond with:

"I couldn't find that information in the uploaded documents."

Keep your answers clear, concise, and accurate.

Also  Keep your response short and concise — 1 to 3 sentences maximum, no long explanations or lists.
Context:
{context}
""",
        ),
        (
            "human",
            "{input}",
        ),
    ]
)
