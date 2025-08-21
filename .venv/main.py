from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))    

app = FastAPI()

class ChatInput(BaseModel):
    user_message: str

@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.post("/chat")
async def chat_endpoint(input: ChatInput):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input.user_message}
            ],
        )
        bot_response = completion.choices[0].message.content
        return {"bot_response": bot_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))