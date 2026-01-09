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

"""
This function is used as a router after all chunsks are processed. It checks for errors, if there is at least one error it will consider the entire processing as failed.
For any error, our ageent should perform a retry.
We define the retry logic later in the workflow.

For successful chunk processing, it will compile all the summaries into a final summary.
In general, this works as a router in conditional edges. So it may return wither "node_error_handler" or "node_generate_summary"
"""
def validate_chunk_response(state: GenCommentState) -> str:
    """
    Router to split chunks to tasks based on processing results.
    If there are errors in processing, route to error handler.
    Otherwise, route to post chunk processing.
    """
    errors = state.get("errors", [])
    if errors:
        logger.debug(f"Routing to error handler for chunk id {state.get('chunk_id')} due to errors.")
        return "node_error_handler"
    else:
        logger.debug("Routing to post chunk processing.")
        return "node_generate_summary"
