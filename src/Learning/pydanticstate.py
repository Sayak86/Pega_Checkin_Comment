from pydantic import BaseModel,Field,field_validator,model_validator
from typing import Any, Dict, Literal,TypedDict
from langgraph.graph import StateGraph,START,END



class PydanticState(BaseModel):
    name:str = Field(description= "Name of the person")
    mood:Literal["happy", "sad"]
    employee_id:str
    country:str 
    department:str = Field(default="General",description="Department of the person")

    @field_validator("mood")
    @classmethod
    def validate_mood(cls, v):
        if v not in ["happy", "sad"]:
            raise ValueError("mood must be either 'happy' or 'sad'")
        return v
    
    @model_validator(mode="after")
    def check_employee_id(self):
        if self.country == "India" and self.department == "Finance":
            if not self.employee_id.startswith("IN-FIN-"):
                raise ValueError("For India Finance department, employee_id must start with 'IN-FIN-'")
        return self

    

def node_1(state:PydanticState)->dict:
    return {"name": state.name.capitalize()}
def node_2(state:PydanticState)->dict:
    return {"mood" : "happy"}
def node_3(state:PydanticState)->dict:
    return {"mood" : "sad"}
def check_mood(state:PydanticState)->Literal["node_2", "node_3"]:
    if len(state.name) %2 ==0:
        return "node_2"
    else:
        return "node_3"
def build_pydantic_graph():
    builder = StateGraph(PydanticState)

    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)
    builder.add_node("node_3", node_3)

    builder.add_edge(START, "node_1")
    builder.add_conditional_edges("node_1", check_mood)
    builder.add_edge("node_2", END)
    builder.add_edge("node_3", END)
    return builder.compile()

if __name__ == "__main__":
    initialState = PydanticState(**{"name": "alice", "mood": "sad", "employee_id": "US-FIN-001", "country": "India", "department": "Finance"})

    app = build_pydantic_graph()
    final_state = app.invoke(initialState)
    print(final_state)