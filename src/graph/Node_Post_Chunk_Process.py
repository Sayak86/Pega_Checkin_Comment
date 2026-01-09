from graph.state import GenCommentState
import logging
logger = logging.getLogger("uvicorn")
logging.getLogger("uvicorn").setLevel(logging.DEBUG)

def node_post_process_chunk(state: GenCommentState) -> dict:
    """
    This node starts after each chunks are processd.
    It collects all the summaries from each chunk and compiles a final summary.
    Each chunk summary is a dictionary with keys: chunkId, summaryText, result,numItems
    We are interested to createa final summary having all the summaryText concatenated.
    """
    final_summary = ""
    summaries = state.get("summaries", [])
    logger.debug("-- Post processing chunk summaries --\n")
    for summary in summaries:
        summary_text = summary.get("summaryText", "")
        final_summary += summary_text + "\n"
        logger.debug(f"Chunk ID: {summary.get('chunkId')} Summary: {summary_text}\n")

    