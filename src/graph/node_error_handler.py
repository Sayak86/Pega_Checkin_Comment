from graph.state import GenCommentState
import time
import pprint
from datetime import datetime
import logging
logging.getLogger("uvicorn").setLevel(logging.DEBUG)
logger = logging.getLogger("uvicorn")
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm.llmclient import get_client
from llm.loadPrompt import load_prompt

def node_error_handler(state: GenCommentState) -> list:
    """
    This node handles errors encountered during chunk processing.
    It logs the errors and prepares an error summary.
    """
    errors = state.get("errors", [])
    logger.error(f"-- Error Handler Invoked -- for chunk id {state.get('chunk_id')}\n")


    # Prepare an error summary using LLM, we dont return final summary in case of errors. We will do it later.
    return {"errors": errors}

    
