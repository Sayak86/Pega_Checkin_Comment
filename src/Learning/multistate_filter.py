from langgraph.graph import StateGraph,START,END
from typing import TypedDict, List, Annotated

"""
This example demonstartes how to use multiple states in a graph , and how input and output states can be different for different nodes. 
We will have an overallstate, inputstate and outputstate - input and output state works as the filter on the overall state.
"""

class OverallState(TypedDict):
    question:str
    thought:str
    answer:str

class InputState(TypedDict):
    question:str

class OutputState(TypedDict):
    answer:str

def thinking_node(state:InputState):
    question = state['question']
    thought = f" If one bucket has a capacity of 10 liters and is filled to 70%, then the amount of water in the bucket is 7 liters."""
    answer = "7 liters"
    return {"thought": thought, "answer": answer}  # This will be passed to node_2

def answer_node(state:OverallState)-> OutputState:
    thought = state['thought']
    answer = state['answer']
    return {"answer": f"The answer to the question is: {answer}"}  # This will be passed to node_3

builder = StateGraph(OverallState, input=InputState, output=OutputState)
builder.add_node("thinking_node", thinking_node)
builder.add_node("answer_node", answer_node)
builder.add_edge(START, "thinking_node")
builder.add_edge("thinking_node", "answer_node")
builder.add_edge("answer_node", END)

if __name__ == "__main__":
    initialState:OverallState = {
        "question": "If one bucket has a capacity of 10 liters and is filled to 70%, how much water is in the bucket?"
    }

    app = builder.compile()
    final_state = app.invoke(initialState)
    print("Final state keys:", final_state.keys())
    print("Final state:", final_state)
