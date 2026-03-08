from langgraph.graph import StateGraph,START,END
from typing import TypedDict, List, Annotated

def custom_reducer(existing:dict, new_value:dict)->dict:
    """
    Custom reducer to merge dictionaries.
    """
    print("------------Inside custom reducer/n----------------")
    print(f"Existing state: {existing}")
    print(f"New value: {new_value}")
    if not existing:
        return new_value
    if not new_value:
        return existing
    # Merge the two dictionaries
    for k,v in  new_value.items():
        if k in existing:
            existing[k] += v  # Assuming values are integers and we want to sum them
        else:
            existing[k] = v

    print(f"Updated existing state after merging: {existing}")
    return existing


# define a state
class CustomReducerState(TypedDict):
    items: Annotated[dict, custom_reducer]

def node_1(state:CustomReducerState)->dict:
    return {"items": {"apple": 10, "banana": 5}}  # This will be reduced using custom_reducer

def node_2(state:CustomReducerState)->dict:
    return {"items": {"apple": 3, "orange": 7}}  # This will be reduced using custom_reducer    

def build_custom_reducer_graph():
    builder = StateGraph(CustomReducerState)

    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)

    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", "node_2")
    builder.add_edge("node_2", END)
    return builder.compile()

if __name__ == "__main__":
    initialState:CustomReducerState = {
        "items": {"mango": 2,"grape": 4}
    }

    app = build_custom_reducer_graph()
    final_state = app.invoke(initialState)
    print(final_state)