from langgraph.graph import StateGraph,START,END,MessagesState
from langchain.messages import AIMessage, HumanMessage, SystemMessage,RemoveMessage
from pprint import pprint
from langchain_openai import ChatOpenAI

"""
This code is to demonstate how we can trim and filter messages and chat history using langgraph modules.
Often the chat content grows much and beyond control and hence needs to have a smaller set to maintain 
"""

llm = ChatOpenAI(
    model = "gpt-4.1",
    temperature = 0.2,
    max_tokens = 200
    
)

messages = [AIMessage(content="Hello, how are you?")]
messages.append(HumanMessage(content="I would like to know Orca - the ocean animal, can you tell me about it?"))
messages.append(HumanMessage(content="Absolutelty!May I ask if you have any focus area on Orca?"))
messages.append(HumanMessage(content="I am interested in which places and climate we can find Orcas?"))
messages.append(AIMessage(content="Thanks for the confirmation. Here I will give the details where we can find Orcas."))

def chat_model_mode(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": response}

def cleanup_Messages(state:MessagesState):
    messages = state["messages"]
    # delete all but last 2
    to_remove = [RemoveMessage(m.id) for m in messages[:-2]]
    return {"messages": to_remove}




builder = StateGraph(MessagesState)
builder.add_node("chat_model", chat_model_mode)
builder.add_edge(START, "chat_model")
builder.add_edge("chat_model", END)

graph = builder.compile()

result = graph.invoke({"messages": messages})

for msg in result["messages"]:
    msg.pretty_print()