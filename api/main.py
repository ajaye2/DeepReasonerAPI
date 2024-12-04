from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.responses import StreamingResponse
from reasoners.lm import OpenAIModel
from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

MODEL_NAME = os.getenv("MODEL_NAME")

class ChainOfThoughtRequest(BaseModel):
    prompt: str
    temperature: float | None = 1.0

@app.get("/")
def root():
    return {"message": "Welcome to DeepReasonAPI"}

@app.get("/stream")
async def stream_intermediate_states():
    async def fake_streamer():
        for i in range(1, 6):
            yield f"Processing chunk {i}\n"
    return StreamingResponse(fake_streamer(), media_type="text/plain")

@app.post("/chain_of_thought")
def chain_of_thought(request: ChainOfThoughtRequest):
    try:
        model = OpenAIModel(model=MODEL_NAME, use_azure=True)
        
        prompt = "Let's think step by step. \n" + request.prompt

        response = model.generate(
            [prompt],
            temperature=request.temperature
        ).text[0]
        
        return {
            "response": response,
        }
    except Exception as e:
        raise HTTPException(status_code=500)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=3100)
