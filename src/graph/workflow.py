from typing import Any, Dict
from langgraph.graph import StateGraph,START,END
from marshmallow import pprint
from graph.node_perform_chunk import node_perform_chunk
from graph.router_split_Chunks_To_Task import router_split_chunks_to_tasks
from graph.node_process_each_chunk import node_process_each_chunk
from graph.state import GenCommentState
from graph.validate_route_response import validate_chunk_response
from graph.node_error_handler import node_error_handler
from graph.node_generate_summary import node_generate_summary

import uvicorn,logging,pprint
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
    # Step 3: Add node for error handling
    graph.add_node("node_error_handler", node_error_handler)
    # Step 4: Add node to generate final summary
    graph.add_node("node_generate_summary", node_generate_summary)



    # Define edges
    graph.add_edge(START, "node_perform_chunk")
    graph.add_conditional_edges("node_perform_chunk", router_split_chunks_to_tasks)
    graph.add_conditional_edges("node_process_each_chunk", validate_chunk_response)
    graph.add_edge("node_error_handler", END)
    graph.add_edge("node_generate_summary", END)

    # Compile the graph
    app = graph.compile()

    # Run the graph with initial state
    final_state = app.invoke(graph_state)

    # If errors, then return the errors
    errors = final_state.get("errors", [])
    if errors:
        sanitized_errors = []

        # remove chunk_data from error
        for error in errors:
            sanitized_errors.append({k:v for k,v in error.items() if k!="chunk_data"})
        logger.error(f"Errors encountered during chunk processing: {pprint.pformat(sanitized_errors)}")
        return sanitized_errors
    
    # Otherwise return the final summary
    final_summary = final_state.get("final_summary")
    logger.debug(f"Workflow completed with with result as \n {final_state}.")
    return final_summary





