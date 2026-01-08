from graph.state import GenCommentState
import logging
logger = logging.getLogger("uvicorn")
logging.getLogger("uvicorn").setLevel(logging.DEBUG)

def node_post_process_chunk(state: GenCommentState) -> dict:
    """
    This node starts after each chunks are processd.
    It collects all the summaries from each chunk and compiles a final summary.
    Each cunk summary is a dictionary with keys: chunkId, summaryText, result,numItems
    We are interested to createa final summary having c
    """
    final_summary = ""
    summaries = state.get("summaries", [])
    logger.debug("-- Post processing chunk summaries --\n")
    logger.debug(summaries)

    # catch errors
    errors = state.get("errors", [])
    logger.debug(f"Errors encountered during chunk processing: {errors[0].get('error')}")
    for error in errors:
        final_summary += f"Error in chunk {error.get('chunk_id')}: {error.get('error')}\n"
    return {"final_summary": final_summary}

    