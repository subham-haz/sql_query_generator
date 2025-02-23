from fastapi import FastAPI
from pydantic import BaseModel
from app.chatbot import process_query

app = FastAPI()

# Define request model
class QueryRequest(BaseModel):
    user_input: str

@app.post("/chat/")
async def chat(request: QueryRequest):
    """Chatbot endpoint: Convert user input to SQL and fetch results"""
    response = process_query(request.user_input)
    # print(response)
    return response
