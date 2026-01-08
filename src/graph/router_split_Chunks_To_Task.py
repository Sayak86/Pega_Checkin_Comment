from graph.state import GenCommentState
from langgraph.graph import StateGraph,  START, END
from langgraph.types import Send


def router_split_chunks_to_tasks(state: GenCommentState) -> list[Send]:
    """
    Split each chunk into seoerate tasks. 
    For parallel processingof chunks we use Send type.
    """

    chunks = state['chunks']
    tasks = []
    ruleType = state.get("ruleType", "UnknownRuleType")
    for idx, chunk in enumerate(chunks):
        tasks.append(
            Send(
                node="node_process_each_chunk",
                arg={
                    "chunk": chunk,
                    "chunk_id": idx,
                    "ruleType": ruleType
                }
            )
        )
    return tasks