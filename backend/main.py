from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a drive-thru assistant. Always respond in JSON with burgers, fries, drinks."},
            {"role": "user", "content": order_request.order}
        ]
    )

    result = response.choices[0].message.content

    return {"placed_order": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
