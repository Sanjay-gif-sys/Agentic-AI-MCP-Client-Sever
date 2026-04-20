class LLMService:
    async def generate_response(self, query: str, context: str) -> str:
        return (
            f"User Query: {query}\n\n"
            f"Based on the gathered evidence:\n{context}"
        )