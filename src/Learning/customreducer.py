from pydantic import BaseModel,Field,field_validator,model_validator
from typing import Any, Dict, Literal,TypedDict,List, Annotated
from langgraph.graph import StateGraph,START,END

def custom_reducer(existing:List[int], new_value:int | List[int])->List[int]:
    """
    Custom reducer to accumulate integers into a list.
    """
    if isinstance(new_value, list):
        print(f"New value is a list.Reducing list {new_value} into existing {existing}")
        return existing + new_value
    else:
        print(f"New value is an int.Reducing value {new_value} into existing {existing}")
        return [val*new_value for val in existing]
    


class CustomReducerState(TypedDict):
    name:str
    numbers: Annotated[List[int], custom_reducer]
    next_number:int


def node_1(state:CustomReducerState)->dict:
    state['name'] = "India"   
    return {"numbers": state["next_number"]}  # This will be reduced using custom_reducer

def node_2(state:CustomReducerState)->dict:
    state['name'] = "USA"   
    return {"numbers": [100,200]}  # This will be reduced using custom_reducer

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
        "name": "alice",
        "numbers": [10,12],
        "next_number": 5
    }

    app = build_custom_reducer_graph()
    final_state = app.invoke({
        "name": "alice",
        "numbers": [10,12],
        "next_number": 5
    })
    print(final_state)


