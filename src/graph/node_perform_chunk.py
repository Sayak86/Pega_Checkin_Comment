from chunk.pxResults_chunker import get_chunks,chunk_pxResults
from graph.state import GenCommentState

def node_perform_chunk(graphState: GenCommentState) -> dict:
    """
    Get the json of rule comparison results and split that into adaptive chunks.
    Also calculate total chunks and total changes for context.
    """
    ruleType = graphState.get("ruleType", "UnknownRuleType")
    comparedResultsJson = graphState.get("comparedResultsJson", {})

    chunks = chunk_pxResults(comparedResultsJson)
    total_chunks = len(chunks)
    total_changes = len(comparedResultsJson.get("pxResults", []))

    return {
        "chunks": chunks,
        "ruleType": ruleType,
        "total_chunks": total_chunks,
        "total_changes": total_changes,
    }


if __name__ == "__main__":
    print("Node perform chunk module loaded.")