from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda,RunnablePassthrough,RunnableMap
from langchain_core.prompts import ChatPromptTemplate,ChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser,SimpleJsonOutputParser
from llm.loadPrompt import load_prompt
from config import load_config
from dotenv import load_dotenv
import os
from llm.llmresponsemodel import ChunkReponseModel
"""
    Here we will build the chain for LLM execution
"""

def get_client()->ChatOpenAI:
    """
    Returns a llm instance
    """
    
    
    # Reads the API key from .env file
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")

    
    # Load LLM configuration
    config = load_config()
    llm_config = config['llm_config']
    llm = ChatOpenAI(
        model=llm_config['model'],
        temperature=llm_config['temperature'],
        max_tokens=llm_config['max_tokens'],

    ).with_structured_output(ChunkReponseModel)
    return llm


    


