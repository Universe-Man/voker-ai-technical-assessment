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

order_counter = 0

@app.post("/place-order")
async def place_order(order_request: OrderRequest):
    """Take a text order, send to OpenAI, return structured result."""

    message = """You are a drive-thru assistant. Always respond in JSON with exactly these keys: 
    {
        "order_number": <integer>,
        "burgers": <integer>,
        "fries": <integer>,
        "drinks": <integer>,
        "valid": <boolean>
    }.
    Never omit a key. Always return integers (0 if none). Do not add extra text or explanation. Order numbers should start at 1 and increment for each request. If an order is place set valid to true. If an order is canceled set valid to false. If they use an order number when canceling an order, set that number as order_number. If they don't provide a number, set order_number to 0."""

    global order_counter

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": message},
            {"role": "user", "content": order_request.order}
        ]
    )

    cleaned_res = re.sub(r"```json|```", "", response.choices[0].message.content).strip()

    res = json.loads(cleaned_res)

    if res["valid"]:
        order_counter += 1
        current_order_number = order_counter
    else:
        current_order_number = res["order_number"]

    return {
            "placed_order":
                {
                    "order_number": current_order_number,
                    "burgers": res["burgers"],
                    "fries": res["fries"],
                    "drinks": res["drinks"],
                    "valid": res["valid"]
                }
            }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
