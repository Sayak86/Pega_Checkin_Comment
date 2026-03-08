from langgraph.graph import StateGraph,START,END
from typing import TypedDict, List, Annotated

class OverallState(TypedDict):
    country:str

class PrivateState(TypedDict):
    capital:str

def node_1(state:OverallState)->PrivateState:
    country = state['country']
    return {"capital": "Delhi"}  # This will be passed to node_2

def node_2(state:PrivateState)-> OverallState:
    capital = state['capital']
    return {"country": f"the city  {capital} is in India"}  # This will be passed to node_3

builder = StateGraph(OverallState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)

if __name__ == "__main__":
    initialState:OverallState = {
        "country": "India"
    }

    app = builder.compile()
    final_state = app.invoke(initialState)
    print(final_state)