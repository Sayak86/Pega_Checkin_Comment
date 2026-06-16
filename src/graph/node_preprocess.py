from graph.state import GenCommentState
from chunk.preprocess_chunk import preprocess_pxresults
import logging

logger = logging.getLogger("uvicorn")


def node_preprocess(state: GenCommentState) -> dict:
    raw_json = state["comparedResultsJson"]
    logger.debug(f"[Preprocess] Enriching {len(raw_json.get('pxResults', []))} pxResults with resolved_path")

    enriched = preprocess_pxresults(raw_json)

    logger.debug("[Preprocess] Done — resolved_path injected, noise fields stripped")
    return {"comparedResultsJson": enriched}
