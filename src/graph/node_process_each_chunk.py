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

def node_process_each_chunk(state: GenCommentState) -> dict:
    """
    Process each chunk of comparison results.
    This function simulates processing by summarizing the chunk.
    """
    chunk = state['chunk']
    chunk_id = state["chunk_id"]
    ruleType = state["ruleType"]

    # Log the start of processing with a timestamp
    start_time = datetime.now()
    logger.debug(f"[START] Processing chunk {chunk_id} at {start_time}. RuleType: {ruleType}")

    try:
        # Step 1 - instantiate LLM client
        llm = get_client()

        # Step 2 - load prompt template
        prompt_template = load_prompt(ruleType)

        # Step 3 - Create a chain
        chain = prompt_template | llm 

        # Step 4 - Execute the chain
        result = chain.invoke({
            "chunk_data": chunk,
            "chunk_id": chunk_id,
        })

        # Step 5 - Convert pydantic model to dict if needed
        if hasattr(result, 'model_dump'):
            result = result.model_dump()

        # Map LLM fields to expected fields
        result = {
        "chunkId": result.get("chunk_id"),  # or chunk_id depending on LLM output
        "summaryText": result.get("changeSummary")  # or the actual field name
    }

        # Log the end of processing with a timestamp
        end_time = datetime.now()
        logger.debug(f"[END] Processed chunk {chunk_id} at {end_time}. Duration: {end_time - start_time}")

        return {"summaries": [result]}
    except Exception as e:
        
        errorDef = {"chunk_id": chunk_id, "error": str(e), "chunk_data": chunk}
        return {"errors": [errorDef]}