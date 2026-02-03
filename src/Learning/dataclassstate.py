from dataclasses import dataclass,field,fields
from typing import Literal
from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt.tool_node import ToolNode
from random import random,randint

"""
Here we use dataclass as state definition, not TypeDict.
How to do 
1. We need to import the dataclass and field from dataclasses module.
2. Define a dataclass with the required fields.
3. Use the dataclass as the state type in StateGraph.
The graph will pass the dataclass instance to each node function.
To invoke the graph, create an instance of the dataclass with initial values.
To define the state and to access the fields, use standard dataclass syntax which is classobject.fieldname

Regardless of whether your state is TypedDict or dataclass, nodes must return a dictionary. LangGraph merges the returned dict into the state.


"""


@dataclass
class DataClassState:
    name:str
    mood:Literal["happy", "sad"]= field(default="testing")


def node_1(state:DataClassState)->dict:
    return {"name": state.name.capitalize()}

def node_2(state:DataClassState)->dict:
    return {"mood" : "happy"}

def node_3(state:DataClassState)->dict:
    return {"mood" : "sad"}

def check_mood(state:DataClassState)->Literal["node_2", "node_3"]:
    if randint(10,30) %2 ==0:
        return "node_2"
    else:
        return "node_3"

def build_dataclass_graph():
    builder = StateGraph(DataClassState)


    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)
    builder.add_node("node_3", node_3)

    builder.add_edge(START, "node_1")
    builder.add_conditional_edges("node_1", check_mood)
    builder.add_edge("node_2", END)
    builder.add_edge("node_3", END)
    return builder.compile()

if __name__ == "__main__":
    initialState = DataClassState(name="alice")
    app = build_dataclass_graph()
    finalState = app.invoke(initialState)
    print(finalState)


