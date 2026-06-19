from graph.state import GenCommentState
from langgraph.graph import StateGraph,  START, END
from langgraph.types import Send


def router_split_chunks_to_tasks(state: GenCommentState) -> list[Send]:
    """
    Split each chunk into separate tasks.
    For parallel processing of chunks we use Send type.
    Add chunk context so each chunk knows its position in the overall batch.
    """

    chunks = state['chunks']
    total_chunks = state.get("total_chunks", len(chunks))
    total_changes = state.get("total_changes", sum(len(c) for c in chunks))
    tasks = []
    ruleType = state.get("ruleType", "UnknownRuleType")

    change_idx = 0
    for idx, chunk in enumerate(chunks):
        chunk_size = len(chunk)
        start_idx = change_idx + 1
        end_idx = change_idx + chunk_size
        chunk_context = f"Chunk {idx+1} of {total_chunks}, changes {start_idx}-{end_idx} of {total_changes} total"

        tasks.append(
            Send(
                node="node_process_each_chunk",
                arg={
                    "chunk": chunk,
                    "chunk_id": idx,
                    "ruleType": ruleType,
                    "chunk_context": chunk_context,
                }
            )
        )
        change_idx += chunk_size

    return tasks