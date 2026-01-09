from typing import TypedDict, List, Literal, Dict, Any, Annotated
import operator
"""
The entire JSON is splittled into chunks based on the number of pxResults.
Each Chunk will have a list of pxResult.
Each pxResult is a dictionary.

So the final structure will be like this:
{
    "chunks": [
        [pxResult1, pxResult2, ...],  # Chunk 1 with list of pxResults
        [pxResultN, pxResultM, ...],  # Chunk 2 with list of pxResults
        ... 
    ]
}  

So chunks are list of list of pxResult.
chunks = List[List[pxResult]] -- all my chunks
chunk = List[pxResult]        -- a single chunk
pxResult = Dict[str, Any]     -- a single pxResult

"""
# Define a type for pxResult -- a single pxResult
pxResult = Dict[str, Any]
# error are list of error dictionaries, error dictionary may have keys like "chunkId", "errorMessage", "chunk".
errorDef = Dict[str, Any]


class GenCommentState(TypedDict):
    comparedResultsJson: Dict[str, Any]
    chunks: List[List[pxResult]] # Chunks are collection of chunk
    chunk: List[pxResult]      # A single chunk
    chunk_id: int # ID of the chunk being processed
    summaries: Annotated[List[dict[str, Any]], operator.add]  # List of summaries for each chunk
    final_summary: str
    ruleType:str
    errors: Annotated[List[errorDef], operator.add]


