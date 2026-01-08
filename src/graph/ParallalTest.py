from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph,START,END
from typing import TypedDict, List, Literal, Dict, Any, Annotated
import operator
import time
from time import sleep

class ParallalTest(TypedDict):
    topics : Annotated[List[str],operator.add]

# I will add one tiger and one lion node
# I will add them in parallel and then add to the topics
startTime = time.time()
def tiger(state:ParallalTest)->ParallalTest:
    sleep(5)
    return {"topics" : ["tiger"]}

def lion(state:ParallalTest)->ParallalTest:
    sleep(5)
    return {"topics" : ["lion"]}

def llmExecution(input:str,RuleType:str)->str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
    




graph = StateGraph(ParallalTest)
graph.add_node("tiger",tiger)
graph.add_node("lion",lion)

graph.add_edge(START,"tiger")
graph.add_edge(START,"lion")
graph.add_edge("tiger",END)
graph.add_edge("lion",END)

app = graph.compile()
result = app.invoke(
    {"topics": ["Animals"]}
)

endTime = time.time()
print("Total time taken:",endTime - startTime)
print(result)