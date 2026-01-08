"""
Here we will chunk the diff JSON between 2 rules.
Each defiiference between 2 versions of one rule are stored in the pxResults pagelist.
If the number of pxResults are too high then we must go for chunking in order to accommodate all the data.
Otherwise we will face the rate limit of the LLM we are using.
We use an daptive chunking logic here
    If the pxResults are less than 5 we will not chunk them.
    If the pxResults are between 5 and 20 we will chunk them into 2 chunks.
    If the pxResults are between 20 and 50 we will chunk them into 5 chunks.
    If the pxResults are more than 50 we will chunk them into 10 chunks.
"""
import json
from pathlib import Path

def read_json_file(file_name: str) -> dict:
    # Always read the file from data folder
    if file_name is None:
        raise ValueError("file_name cannot be None")
    
    if file_name[-5:] != ".json":
        raise ValueError("file_name must be a json file")
    
    path = Path(__file__).parent.parent.parent.resolve()
    path = path / "data" / file_name
    
    # Now we will read the json file
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_name} does not exist in the data folder.")
    except json.JSONDecodeError:
        raise ValueError(f"The file {file_name} is not a valid JSON file.")
    
# Start chunking logic
def chunk_pxResults(RuleDiffData: dict) -> list:
    pxResults = RuleDiffData.get("pxResults", [])
    num_results = len(pxResults)
    
    if num_results == 0:
        return []
    elif num_results < 5:
        return [pxResults]
    elif num_results <= 20:
        chunk_size = (num_results + 1) // 2
    elif num_results <= 50:
        chunk_size = (num_results + 4) // 5
    else:
        chunk_size = (num_results + 9) // 10
    
    chunks = [pxResults[i:i + chunk_size] for i in range(0, num_results, chunk_size)]
    return chunks

# Get Chunks
def get_chunks(file_name: str) -> list:
    RuleDiffData = read_json_file(file_name)
    chunks = chunk_pxResults(RuleDiffData)
    return chunks
