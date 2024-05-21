from fastapi import FastAPI, Query
from typing import List, Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


origins = json.loads(os.getenv("ALLOWED_ORIGINS", '[]'))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchResult(BaseModel):
    id:str
    title: str
    summary: str
    url: str

class SearchTip(BaseModel):
    id:str
    tip: str

@app.get("/")
async def read_root():
    environment = os.getenv("ENVIRONMENT", "production")  # Default to production if not set
    message = "Hello from local backend." if environment == "development" else "Hello from production backend."
    print(message)
    return {"message": message}

@app.get("/search", response_model=List[SearchResult])
async def search(query: Optional[str] = Query(None, min_length=3, max_length=50)):
    #TODO: Replaced simulated search response with rag query
    print(query)
    results = [
        SearchResult(id="1", title="Title of Doc1", summary="This document explores top-rated utilities renowned for their quality and service.", url="https://example.com/doc1"),
        SearchResult(id="2", title="Title of Doc1", summary="Learn about the science behind the electric grid.", url="https://example.com/doc2")
    ]
    return results


@app.get("/search-tips", response_model=List[SearchTip])
async def tips(query: Optional[str] = Query(None, max_length=50)):
    print(f"Search Tips requested for... {query}")
    search_tips = []
    if len(query or "") < 10:
        search_tips = [
            SearchTip(id="0", tip="Which document talks about top-rated utilities?"),
        ]
    elif len(query or "") >= 10:
        search_tips = [
            SearchTip(id="0", tip="Which document talks about top-rated utilities?"),
            SearchTip(id="1", tip="How does electricity work?")
        ]        
    return search_tips