# main.py
import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# 1. Setup Google Gemini
# We get the key from the "Environment Variable" (secure storage)
# REPLACE "AIza..." WITH YOUR ACTUAL KEY
genai.configure(api_key="AIzaSyD......your_real_key_here")
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI()

# 2. Allow the frontend to talk to us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Your Free "Database"
# Paste your property details here.
PROPERTIES = """
- 10 Downing St, London: £5,000,000. 5 Beds. Available. Historic location.
- 221B Baker St, London: £850,000. 2 Beds. Under Offer. Famous detective lived here.
- 742 Evergreen Tce, Springfield: £400,000. 4 Beds. Available. Pink walls.
"""

class UserMessage(BaseModel):
    message: str

@app.get("/")
def home():
    return {"status": "Alive"}

@app.post("/chat")
def chat_agent(user_input: UserMessage):
    prompt = f"""
    You are a polite estate agent assistant for 'Prestige Estates'.
    Use ONLY this property list to answer questions. If a house isn't listed, say you don't know.
    
    Property List:
    {PROPERTIES}
    
    User: {user_input.message}
    Agent:
    """
    try:
        response = model.generate_content(prompt)
        return {"reply": response.text}
    except Exception as e:
        print(e)
        return {"reply": "I am having trouble connecting to the AI right now."}
