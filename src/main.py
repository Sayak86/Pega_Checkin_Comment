# Import read_json_file from chunk.pxResults_chunker.py
import json
from chunk.pxResults_chunker import get_chunks
import sys
from config import load_config
import pprint
from llm.loadPrompt import load_prompt
from llm.llmclient import get_client
from graph.workflow import wokflow_process
from api import app as fastapi_app
import uvicorn
config = load_config()


if __name__ == "__main__":
    # Run the FastAPI app

    uvicorn.run(fastapi_app, reload=True)

    


