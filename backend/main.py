from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class OrderRequest(BaseModel):
    order: str

@app.post("/place-order")
async def place_order(order_request: OrderRequest):
    """Take a text order, send to OpenAI, return structured result."""

    message = """You are a drive-thru assistant. Always respond in JSON with exactly these keys: 
    {
        "burgers": <integer>,
        "fries": <integer>,
        "drinks": <integer>
    }.
    Never omit a key. Always return integers (0 if none). Do not add extra text or explanation.""" 


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": message},
            {"role": "user", "content": order_request.order}
        ]
    )

    cleaned_res = re.sub(r"```json|```", "", response.choices[0].message.content).strip()

    result = json.loads(cleaned_res)

    return {"placed_order": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
