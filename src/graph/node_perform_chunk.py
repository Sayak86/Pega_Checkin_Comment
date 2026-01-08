from chunk.pxResults_chunker import get_chunks,chunk_pxResults
from graph.state import GenCommentState

def node_perform_chunk(graphState: GenCommentState) -> dict:
    """
    Get the json of rule comparison results and split that into adaptive chunks.
    """
    ruleType = graphState.get("ruleType", "UnknownRuleType")
    comparedResultsJson = graphState.get("comparedResultsJson", {})

    chunks = chunk_pxResults(comparedResultsJson)
    return {"chunks": chunks, "ruleType": ruleType}


if __name__ == "__main__":
    print("Node perform chunk module loaded.")