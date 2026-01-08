from typing import Any, Dict
from langgraph.graph import StateGraph,START,END
from graph.node_perform_chunk import node_perform_chunk
from graph.router_split_Chunks_To_Task import router_split_chunks_to_tasks
from graph.node_process_each_chunk import node_process_each_chunk
from graph.state import GenCommentState
from graph.Node_Post_Chunk_Process import node_post_process_chunk
import uvicorn,logging
logger = logging.getLogger("uvicorn")



def wokflow_process(comparedResultsJson: Dict[str, Any], ruleType: str) -> str:

    logger.debug(f"Workflow Processed for rule type {ruleType} with {len(comparedResultsJson)} items.")

    # Initialize graph state
    graph_state = GenCommentState()
    graph_state["comparedResultsJson"] = comparedResultsJson
    graph_state["ruleType"] = ruleType

    # logging


    # Step 1: Add first node to perform chunking
    graph = StateGraph(GenCommentState)
    graph.add_node("node_perform_chunk", node_perform_chunk)
    # Step 2: Add node to process each chunk
    graph.add_node("node_process_each_chunk", node_process_each_chunk)
    # Step 3: Add post chunk processing node
    graph.add_node("node_post_process_chunk", node_post_process_chunk)

    # Define edges
    graph.add_edge(START, "node_perform_chunk")
    graph.add_conditional_edges("node_perform_chunk", router_split_chunks_to_tasks)
    graph.add_edge("node_process_each_chunk", "node_post_process_chunk")
    graph.add_edge("node_post_process_chunk", END)

    # Compile the graph
    app = graph.compile()

    # Run the graph with initial state
    final_state = app.invoke(graph_state)
    chunks = final_state.get("chunks", [])
    final_summary = final_state.get("final_summary")
    logger.debug(f"Workflow completed with with result as \n {final_state}.")
    return final_summary





