# main.py
import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# 1. Setup Google Gemini
# We get the key from the "Environment Variable" (secure storage)
# REPLACE "AIza..." WITH YOUR ACTUAL KEY
genai.configure(api_key="AIzaSyB0b-U1K4uIKZVnQx_ZCl4TO8cg1XP11uQ")
model = genai.GenerativeModel('gemini-2.5-flash')

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
    history: str = ""

@app.get("/")
def home():
    return {"status": "Alive"}

@app.post("/chat")
def chat_agent(user_input: UserMessage):
    # 1. THE BRAIN UPGRADE (Paste this over your old prompt)
    prompt = f"""
    You are 'Sarah', a Senior Estate Agent at Prestige Estates.
    
    YOUR GOAL:
    Your only goal is to get the user to book a viewing.
    
    YOUR KNOWLEDGE BASE (Only sell these houses):
    {PROPERTIES}
    
    RULES OF ENGAGEMENT:
    1. Be friendly but professional. Use emojis sparingly (🏡).
    2. If the user says the price is too high, gently remind them of the features (location, size).
    3. If the user asks about a house NOT on the list, say: "We don't have that right now, but House #1 is similar."
    4. NEVER invent facts. If it doesn't say the house has a pool, assume it does not.
    5. SHORT ANSWERS. People are reading this on their phones. Keep it under 50 words.

    Always end your answer with a question that moves them forward, like 'Would you like to see photos?' or 'Is there a time you would like to view the property?'"
    
    CONVERSATION HISTORY:
    {user_input.history}
    User: {user_input.message}
    Sarah:
    """
 
    
    return jsonify({'reply': response.choices[0].text.strip()})

    try:
        response = model.generate_content(prompt)
        return {"reply": response.text}
    except Exception as e:
        print(e)
        return {"reply": "I'm thinking..."}
