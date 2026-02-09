from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from generator import URLGenerator
from config import settings

class DomainResponse(BaseModel):
    domain: str

app = FastAPI(
    title="Domain Generator API",
    description="API for generating domain URLs based on user ID and search keyword",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # https://www.autoboost.marketing
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["X-API-Key", "Content-Type"],
)

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    if not api_key or api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key

url_generator = URLGenerator()

@app.get("/get-website-domains", response_model=List[DomainResponse])
async def generate_domains(
    user_id: str, 
    search_keyword: str,
    _: str = Depends(verify_api_key)
):
    if not user_id or not search_keyword:
        raise HTTPException(status_code=400, detail="user_id and search_keyword are required")
    
    search_keyword = search_keyword.strip()
    if len(search_keyword) < 2:
        raise HTTPException(status_code=400, detail="search_keyword must be at least 2 characters")
    
    try:
        domains = url_generator.generate_urls(user_id, search_keyword)
        return domains if domains else []
    except Exception:
        raise HTTPException(status_code=500, detail="Error generating domains")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"status": "Domain Generator API is running"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
