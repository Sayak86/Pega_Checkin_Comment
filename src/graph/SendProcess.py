import json
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from typing import TypedDict, List,Annotated
import operator
import time
from time import sleep

class MainState(TypedDict):
    inputSeries: list[int]
    outputSeries: Annotated[List[int], operator.add]


def node_process_one_number(state:MainState)->dict:
    sleep(2)  # Simulate some processing time
    number = state["inputSeries"][0]
    output = number * 2
    print(f"Processed number: {number}, result: {output}")
    return {"outputSeries": [output]}

# Create a split function, this uses Send
def split_into_tasks(state:MainState)->list[Send]:
    tasks = []
    numbers = state["inputSeries"]
    for num in numbers:
        tasks.append(
            Send(
                node="node_process_one_number",
                arg= {
                    "inputSeries": [num]
                }
            )
        )
    return tasks

def node_collect_results(state:MainState)->dict:
    results = state["outputSeries"]
    print(f"All tasks are completed with result {results}")
    return {}


graph = StateGraph(MainState)

graph.add_node("node_process_one_number",node_process_one_number)
graph.add_node("node_collect_results",node_collect_results)
graph.add_node("split_into_tasks",split_into_tasks)

# Parallel tasks
graph.add_conditional_edges(START, split_into_tasks)

# After all parallel tasks complete, collect results
graph.add_edge("node_process_one_number", "node_collect_results")
graph.add_edge("node_collect_results", END)

initial_state = {
        "inputSeries": [1, 2, 3, 4, 5],
        "outputSeries": []
    }

app = graph.compile()
startTime = time.time()
final_state = app.invoke(
    initial_state
)
endTime = time.time()
print("Total time taken:", endTime - startTime)
print("Final state:", final_state)

