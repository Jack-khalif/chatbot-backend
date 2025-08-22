from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class ChatInput(BaseModel):
    user_message: str

@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.post("/chat")
async def chat_endpoint(input: ChatInput):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input.user_message}
            ],
        )
        bot_response = completion.choices[0].message["content"]
        return {"bot_response": bot_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
