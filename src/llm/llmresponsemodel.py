from pydantic import BaseModel,Field

class ChunkReponseModel(BaseModel):
    chunk_id:str = Field(description="Unique identifier for the chunk")
    changeSummary:str = Field(description="Summary of changes in the chunk")
    error:str = Field(default="",description="Error message if any during processing")
    retry_count :int = Field(default=0,description="Number of retries attempted")