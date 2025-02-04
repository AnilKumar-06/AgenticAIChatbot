from pydantic import BaseModel
from typing import List
from agent import get_response_from_ai_agent
import uvicorn

class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool


from fastapi import FastAPI
app = FastAPI(title="AI Agent")

ALLOW_MODEL_NAMES = [
    "llama-3.3-70b-versatile",
    "deepseek-r1-distill-llama-70b",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]

@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    API endpoint to interact with chatbot  using langgraph and search tool
    It dynamically selects the model specified in the request
    """
    if request.model_name not in ALLOW_MODEL_NAMES:
        return {"error": "Invalid model name.Kindly select a valid AI model"}
    
    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider
    
    response = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider)
    return response

if __name__=="__main__":
    
    uvicorn.run(app, host="127.0.0.1", port=9999)