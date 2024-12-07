from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from .reasoning_algorithms import REASONING_ALGORITHMS
import logging
from typing import Optional, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="DeepReasonAPI",
    description="API for reasoning using language models",
    version="1.0.0"
)

# Constants
MODEL_NAME = os.getenv("MODEL_NAME")
if not MODEL_NAME:
    raise ValueError("MODEL_NAME environment variable is not set")

class ReasoningRequest(BaseModel):
    prompt: str = Field(..., description="The input prompt for reasoning")
    temperature: Optional[float] = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Temperature for controlling randomness in the output"
    )
    messages: Optional[List[dict]] = Field(
        default=None,
        description="A list of messages to send to the model"
    )
    algorithm: Optional[str] = Field(
        default="chain_of_thought",
        description="The reasoning algorithm to use"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "What is the capital of France?",
                "temperature": 0.7,
                "algorithm": "chain_of_thought"
            }
        }

@app.get("/")
async def root():
    """Root endpoint returning API welcome message"""
    return {"message": "Welcome to DeepReasonAPI", "status": "healthy"}

@app.post("/reason")
async def reason(request: ReasoningRequest):
    """
    Process a reasoning request
    
    Args:
        request (ReasoningRequest): The request containing prompt, temperature, and algorithm
    
    Returns:
        dict: The reasoning response
    
    Raises:
        HTTPException: If processing fails
    """
    try:
        logger.info(f"Processing reasoning request with prompt length: {len(request.prompt)} and algorithm: {request.algorithm}")
        
        if request.algorithm in REASONING_ALGORITHMS:
            reasoner = REASONING_ALGORITHMS[request.algorithm](model_name=MODEL_NAME)
        else:
            raise ValueError(f"Unsupported algorithm: {request.algorithm}")
        
        response = reasoner.reason(
            prompt=request.prompt,
            temperature=request.temperature
        )
        
        logger.info("Successfully processed reasoning request")
        return response
    
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid request parameters: {str(ve)}"
        )
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error occurred"
        )
    
@app.get("/stream")
async def stream_intermediate_states():
    """Endpoint for streaming intermediate processing states"""
    async def fake_streamer():
        try:
            for i in range(1, 6):
                yield f"Processing chunk {i}\n"
        except Exception as e:
            logger.error(f"Error in stream processing: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Error occurred while streaming data"
            )
    
    return StreamingResponse(
        fake_streamer(),
        media_type="text/plain"
    )

def start():
    """Function to start the uvicorn server"""
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=3100,
        reload=True  # Enable auto-reload during development
    )

if __name__ == '__main__':
    start()
