from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from generator import URLGenerator

class DomainResponse(BaseModel):
    domain: str

app = FastAPI(
    title="Domain Generator API",
    description="API for generating domain URLs based on user ID and search keyword",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize URL Generator
url_generator = URLGenerator()

@app.get("/generate-domains/", response_model=List[DomainResponse])
async def generate_domains(user_id: str, search_keyword: str):
    try:
        domains = url_generator.generate_urls(user_id, search_keyword)
        
        if not domains:
            return []
            
        return domains
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating domains: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
