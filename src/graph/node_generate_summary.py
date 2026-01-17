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

def node_generate_summary(state: GenCommentState) -> dict:
    """
    This node generates a final summary after all chunks are processed.
    It collects all the summaries from each chunk and compiles a final summary.
    Each chunk summary is a dictionary with keys: chunkId, summaryText, result,numItems
    We are interested to create a final summary having all the summaryText concatenated.
    """
    final_summary = ""
    summaries = state.get("summaries", [])
    logger.debug("-- Generating final summary from chunk summaries --\n")
    for summary in summaries:
        summary_text = summary.get("summaryText", "")
        final_summary += summary_text + "\n"
        logger.debug(f"Chunk ID: {summary.get('chunkId')} Summary: {summary_text}\n")

    
    logger.debug(f"Final Summary Generated:\n{final_summary}\n")
    return {"final_summary": final_summary}