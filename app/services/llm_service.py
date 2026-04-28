import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()
class LLMService:
    async def generate_response(self, query: str, context: str) -> str:
        
        model_name = os.getenv("MODEL_NAME")
        llm = ChatOpenAI(
            model=model_name,
            temperature=0.2
        )
        
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system","You are an helpful AI assistance. kindly provide the answer based on the context and query provided"),
                ("human","\n\n User Query: {query} \n\n Retrieved Context: {context}")
            ]
        )
        
        chain = prompt | llm
        response = chain.invoke({"query":query,"context":context})
        
        return (
            f"User Query: {query}\n\n"
            f"Based on the gathered evidence:\n{response}"
        )